# User Verifications (fact)

**Table**: `business-intelligence-prod.dbt_user.fact__user_verifications`
**Grain**: One row per verification event (attempt, status change, or revocation)

| Column | Type | Description |
|--------|------|-------------|
| user_id | STRING | Unique user identifier |
| status | STRING | Verification status: `PASSED`, `FAILED`, `REVOKED`, `FACE_RECHECK_REQ` |
| created_at | TIMESTAMP | Timestamp of the verification event |

## Business Logic
- `PASSED`: User successfully completed verification.
- `FAILED`: User's verification attempt was unsuccessful.
- `REVOKED`: Verification was manually removed by an admin.
- `FACE_RECHECK_REQ`: User is required to perform a face re-verification. They are considered **not verified** until they pass this challenge.

**Determining Current Verification Status**:
To find a user's current status, select the row with the most recent `created_at` timestamp for that `user_id`. Only `status = 'PASSED'` on the latest record indicates a currently verified user.


**Table**: `business-intelligence-prod.dbt_user.fact__user_verifications`
**Grain**: One row per verification event (attempt, status change, or revocation)

| Column | Type | Description |
|--------|------|-------------|
| user_id | STRING | Unique user identifier |
| status | STRING | Verification status: `PASSED`, `FAILED`, `REVOKED`, `FACE_RECHECK_REQ` |
| created_at | TIMESTAMP | Timestamp of the verification event |

## Business Logic
- `PASSED`: User successfully completed verification.
- `FAILED`: User's verification attempt was unsuccessful.
- `REVOKED`: Verification was manually removed by an admin.
- `FACE_RECHECK_REQ`: User is required to perform a face re-verification. They are considered **not verified** until they pass this challenge.

**Determining Current Verification Status**:
To find a user's current status, select the row with the most recent `created_at` timestamp for that `user_id`. Only `status = 'PASSED'` on the latest record indicates a currently verified user.