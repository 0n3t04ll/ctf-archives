Medium Crypto
Rayyywater

read readme.md to get started!


*SECURITY AUDIT:* PRNGbreakthrough
*Status:* CRITICAL VULNERABILITY

*Background:*
The vault uses a Linear Congruential Generator (LCG) to create session tokens. 
The recurrence follows this linear formula: 

    Next_Token = (A * Current_Token + C) % M

*Technical Specs:*
- **Modulus (M):** 4294967296 (2^32)
- **Multiplier (A):** Unknown
- **Increment (C):** Unknown

*Mission:*
6 session tokens were intercepted in "vault_logs.txt" 
The 7th token is the Master Override Key. 

Find it and wrap it as: `LNC26{TOKEN}` (9 digits, pad with a leading zero).
