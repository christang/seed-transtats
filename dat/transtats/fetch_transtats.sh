for ((i=2011; i<2013; i++))
do
  for ((j=1; j<13; j++))
  do
    wget http://www.transtats.bts.gov/Download/On_Time_On_Time_Performance_${i}_${j}.zip
  done
done
