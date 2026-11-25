---
name: social-platform-publishing-engine
description: "Use when integrating social OAuth or publishing videos."
version: 1.0.0
author: OPA Engineering
license: MIT
metadata:
  tags: [social, oauth, pkce, publishing, token-vault, aes-256-gcm, multi-channel]
  hermes:
    tags: [social, oauth, pkce, publishing, token-vault, aes-256-gcm, multi-channel]
    related_skills: [video-content-repurposing, video-rendering-engine]
---

# Social Platform Publishing & OAuth Integration Engine

Production engineering patterns for integrating official social media OAuth 2.0 PKCE flows (TikTok, YouTube, Meta Facebook/Instagram, LinkedIn), managing AES-256-GCM encrypted token vaults at rest, dispatching multi-channel video publishing campaigns, enforcing destination-level idempotency, and handling partial failures.

## When to Use

Use when:
- Implementing OAuth 2.0 authorization code flows with PKCE and CSRF state protection.
- Encrypting, decrypting, and rotating social platform access and refresh tokens at rest.
- Dispatching rendered video files to multiple social platforms simultaneously.
- Implementing destination-level idempotency to prevent duplicate posts on social feeds.
- Handling partial multi-platform publishing success and isolated failure retries.

## Procedure: Secure OAuth 2.0 Flow & Token Vault

1. **Cryptographically Secure State & PKCE**:
   - Generate a 32-byte cryptographic random hex `state` (`randomBytes(32).toString('hex')`).
   - Generate PKCE `codeVerifier` (base64url) and compute `codeChallenge` via SHA-256.
   - Persist state bound to `workspaceId`, authenticated `userId`, and `provider` with a strict 10-minute expiration window.
   - Construct authorization URL using registered redirect URIs and requested scopes.

2. **Callback Validation & Anti-Replay Guard**:
   - On callback, look up state record in database.
   - Reject missing, expired, or provider-mismatched states with HTTP 400.
   - **Anti-Replay**: Check `usedAt === null`. Mark state consumed immediately (`UPDATE oauth_states SET usedAt = now`) before making remote token exchange requests.
   - Exchange code with provider using matching `redirectUri` and `codeVerifier`.

3. **AES-256-GCM Token Encryption at Rest**:
   - Never store plaintext access or refresh tokens.
   - Encrypt credentials using authenticated AES-256-GCM with a 96-bit random IV and 128-bit authentication tag:
     ```typescript
     const encAccessToken = JSON.stringify(encryptToken(tokens.accessToken, masterKey));
     const encRefreshToken = tokens.refreshToken
       ? JSON.stringify(encryptToken(tokens.refreshToken, masterKey))
       : null;
     ```
   - Store encrypted payloads in `social_accounts` with a unique constraint on `(workspaceId, platform, externalAccountId)`.

4. **Zero Secret Leakage Invariant**:
   - Never serialize raw database rows containing `encryptedAccessToken` or `encryptedRefreshToken` into API responses.
   - Map output through a sanitized DTO returning only public metadata: `id`, `accountHandle`, `displayName`, `scopes`, `status`, `tokenExpiresAt`.

5. **Token Refresh & Safe Revocation**:
   - Decrypt refresh token in memory only when calling official refresh endpoints.
   - Atomically update rotated access/refresh tokens and recalculate expiration.
   - On disconnect, call provider revocation endpoints (`revokeAuthorization`), blank out stored tokens, and transition status to `disconnected`.

## Procedure: Multi-Channel Publishing & Distribution Flow

1. **Publication Pre-Flight Verification**:
   - Verify that source video exists and has an approved, completed render job (`status === 'completed'`).
   - Ensure the rendered media file exists on disk/storage before creating a publication.
   - Verify all selected destination social accounts are active and `connected` in the current workspace.

2. **Durable Persistence & Idempotency Key**:
   - Create parent `publications` record with state `DRAFT` or `SCHEDULED`.
   - For each target platform, insert a `publication_destinations` record with a unique compound idempotency key:
     $$\text{idempotencyKey} = \text{publicationId} + \text{"\_"} + \text{socialAccountId}$$
   - This database constraint strictly prevents duplicate dispatch jobs even under concurrent requests or double-clicks.

3. **Dispatch Execution & Attempt Auditing**:
   - Transition publication state to `DISPATCHING`.
   - For each destination:
     - If destination `status === 'published'`: **SKIP** (idempotency protection).
     - Transition destination to `uploading`.
     - Decrypt account access token in memory.
     - Call provider adapter `publishVideo({ videoPath, title, caption, hashtags, accessToken })`.
     - On success: set `status = 'published'`, record `externalPostId`, `externalPostUrl`, and `publishedAt`.
     - On failure: set `status = 'failed'`, record `lastErrorCode` and sanitized error message.
     - Record immutable entry in `publication_attempts` for debugging.

4. **Partial Success Reconciliation & Isolated Retry**:
   - Reconcile overall publication state:
     - All destinations published $\rightarrow$ `PUBLISHED`.
     - Some destinations published, some failed $\rightarrow$ `PARTIALLY_PUBLISHED`.
     - All destinations failed $\rightarrow$ `FAILED`.
   - **Isolated Retry Pattern**: When retrying a `PARTIALLY_PUBLISHED` or `FAILED` campaign, re-execute ONLY destinations with `status === 'failed'`. Never re-post to destinations already marked `published`.

5. **Cancellation**:
   - Allow cancellation only from non-terminal states (`SCHEDULED` or `DRAFT`).
   - Transition publication to `CANCELLED` and mark pending destinations as `cancelled`.

---

## Critical Pitfalls & Engineering Rules

1. **Token Leakage via Unfiltered Database Serialization**:
   Returning raw ORM or database records exposes encrypted tokens or IVs to the frontend. Always use a sanitizing projection that strips all credential fields.
2. **Replay Attacks via Unmarked OAuth States**:
   Validating state without recording `usedAt` allows replayed or intercepted callback URLs to trigger duplicate account associations. Always mark state used before token exchange.
3. **Double-Posting on Multi-Destination Retries**:
   Retrying an entire publication batch without checking individual destination status causes successful platforms to receive duplicate video uploads. Always filter destinations by `status === 'failed'` during retries.
4. **Unverified Video Media Dispatch**:
   Initiating social publishing before FFmpeg rendering is fully completed results in zero-byte or corrupt uploads that burn platform API rate limits. Gate publication creation on `render_jobs.status === 'completed'`.
5. **Foreign Key Constraint Failures on Dummy User IDs**:
   Generating an OAuth state with a hardcoded user string (e.g. `'user_admin'`) violates foreign key constraints if that user does not exist in the database. Always extract and bind the authenticated `user.userId`.
