# Plan 003: Handle 401 Unauthorized in API Interceptor

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md` — unless a reviewer dispatched you and told you they
> maintain the index.
>
> **Drift check (run first)**: `git diff --stat b8f4e2b..HEAD -- frontend/src/services/api.ts`
> If any in-scope file changed since this plan was written, compare the
> "Current state" excerpts against the live code before proceeding; on a
> mismatch, treat it as a STOP condition.

## Status

- **Priority**: P2
- **Effort**: S
- **Risk**: LOW
- **Depends on**: none
- **Category**: correctness
- **Planned at**: commit `b8f4e2b`, 2026-07-16

## Why this matters

The Axios instance in the Next.js frontend attaches the JWT token but does not intercept 401 Unauthorized responses. If a user's token expires, API requests will silently fail or cause cryptic UI errors, rather than redirecting the user to the login page or logging them out cleanly.

## Current state

- `frontend/src/services/api.ts` has a request interceptor but no response interceptor to handle errors:
  ```typescript
  // frontend/src/services/api.ts:26
  (error) => {
    return Promise.reject(error);
  }
  ```

## Commands you will need

| Purpose   | Command                  | Expected on success |
|-----------|--------------------------|---------------------|
| Typecheck | `npm run lint` in frontend | exit 0              |

## Scope

**In scope**:
- `frontend/src/services/api.ts`

**Out of scope**:
- Implementing JWT refresh tokens (just handle hard logout on 401).

## Git workflow

- Branch: `advisor/003-handle-api-401`
- Commit message: `fix: add 401 response interceptor to handle expired tokens`

## Steps

### Step 1: Add a response interceptor
In `frontend/src/services/api.ts`, add an `api.interceptors.response.use` block. 
If the error is a 401 Unauthorized, call a logout utility or clear the local storage tokens and redirect the user to `/login`.
Note: Since this is outside a React context, you can safely use `window.location.href = '/login'` if it's a browser environment.

```typescript
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('token');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);
```

**Verify**: `cd frontend && npm run lint` → exits 0 (or no new errors).

## Test plan

- Manual verification is easiest: remove the token from localStorage and navigate around to ensure you are redirected to `/login`.

## Done criteria

- [ ] `api.interceptors.response.use` is added to `frontend/src/services/api.ts`.
- [ ] 401 responses trigger a clear of the token and a redirect to `/login`.
- [ ] `cd frontend && npm run lint` passes without new errors.
- [ ] `plans/README.md` status row updated.

## STOP conditions

Stop and report back (do not improvise) if:
- `api.ts` already has complex response interceptors that this conflicts with.

## Maintenance notes
- Eventually, a refresh token flow should be added here to seamlessly refresh the JWT rather than immediately kicking the user out.
