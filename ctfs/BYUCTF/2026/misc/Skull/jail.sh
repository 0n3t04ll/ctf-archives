#!/ctf/7169d2872cdac0f85b135c02bc20c1a3/bash

export PATH="/tmp"
cd /ctf/19* # the real directory name is a secret, extra security :)
set +x

echo "Welcome to my new bash, sbash, the Safe Bourne Again Shell! There's no exploiting this system"
echo "There's a script in the local directory you can run for the flag if you can bypass that, then you should report that flag"

while true; do
    read -p "safe_bash> " user_input
    
    # Check if input is empty
    [[ -z "$user_input" ]] && continue

    case "$user_input" in 
        *">"*|*"<"*|*";"*|*"&"*|*"$"*|*"("*|*"}"*|*"\`"*|*" "*|*"\t"*|*"\v"*|*"\f"*|*"\r"*|*"*"*|*"."*|*","*|*"="*) echo "bad" && continue;;
    esac

    if [[ ${#user_input} -gt 20 ]]; then
        echo "bad" && continue
    elif [[ "$str2" =~ [^[:ascii:]] ]]; then
        echo "bad" && continue
    elif [[ "$user_input" =~ [[:lower:]] ]]; then
        echo "bad" && continue
    fi

    # Execute only if it's a Bash builtin
    eval "$user_input" 2>/dev/null || echo "command failed"
done
 