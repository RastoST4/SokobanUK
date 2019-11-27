a=1
while :
do
    python sokoban.py testy/test2 $a > /dev/null || exit
    if [ $a == 60 ]
    then
        break
    fi
	minisat "tosat" "result" > /dev/null
    name=""
    while read -r line
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
