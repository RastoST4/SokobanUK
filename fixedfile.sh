a=1
let t1=$(date +%s)
let t2=$(date +%s)
let COUNT=`expr $t2 - $t1`
while :
do
    python SokobanSolver.py testy/test1 $a > /dev/null || exit
    if [ $COUNT -gt 60 ]
    then
        break
    fi
    let t2=$(date +%s)
    let COUNT=`expr $t2 - $t1`
minisat "tosat" "result" > /dev/null
    name=""
    while IFS = read -r line
do
        name=$line
        if [ $name == "UNSATISFIABLE" ]
        then
            echo "UNSATISFIABLE for $a states"
            break
        fi
   if [ $name != "UNSATISFIABLE" ]
        then
            name="SATISFIABLE"
            break
    fi
done < "result"
    if [ $name == "SATISFIABLE" ]
        then
            echo "SATISFIABLE for $a states"
            break
        fi
    let a+=1
done