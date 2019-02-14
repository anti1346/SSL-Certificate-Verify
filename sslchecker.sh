#/bin/sh 

### function
date2stamp () {
    date --utc --date "$1" +%s
}

stamp2date (){
    date --utc --date "1970-01-01 $1 sec" "+%Y-%m-%d %T"
}

dateDiff (){
    case $1 in
        -s)   sec=1;      shift;;
        -m)   sec=60;     shift;;
        -h)   sec=3600;   shift;;
        -d)   sec=86400;  shift;;
        *)    sec=86400;;
    esac

    dte1=$(date2stamp $1)
    dte2=$(date2stamp $2)
    diffSec=$((dte2-dte1))
    if ((diffSec < 0)); then abs=-1; else abs=1; fi
    echo $((diffSec/sec*abs))  
}

sslchk(){

_DOMAINLIST=`cat domain_list.txt`

for domainlist in $_DOMAINLIST
        do

        _today=`date +'%Y-%m-%d'`
        _VIP=`dig $domainlist +short | paste -sd ","`
        _ED=`./ssl-cert-info.sh --host $domainlist --end | awk {'print $1'}`
        _expire_date=`date -d "$_ED" +'%Y-%m-%d'`
        _expire_day=`dateDiff -d "$_today" "$_expire_date"`

        if [ $_expire_day -le 90 ] ; then  
		#printf "| %-20s | %-65s | %-15s | %-14s |\n" "$domainlist" "$_VIP" "$_expire_day"  "$_ED"
		printf "<tr><td>$domainlist</td><td>$_VIP</td><td>$_expire_day</td><td>$_ED</td></td>\n" "$domainlist" "$_VIP" "$_expire_day" "$_ED"
        fi

done
}

### call function
#sslchk > result.txt

### html
cat <<EOF > result.html
<html>
<head>
<meta http-equiv="Content-Type" content="text/html\; charset=utf-8" />
</head>
<body>
<style>
  table {
    width: 60%;
    border-top: 1px solid #444444;
    border-collapse: collapse;
  }
  th, td {
    border-bottom: 1px solid #444444;
    padding: 10px;
    text-align: center;
  }
  th {
    background-color: #e3f2fd;
  }
  td {
    background-color: #000000;
  }
</style>

<table border="1px">
	<thead>
		<tr><th>도메인</th><th>IP</th><th>만료일 (days)</th><th>만료날짜 (date)</th></tr>
	</thead>
	<tbody>
EOF

sslchk >> result.html

cat <<EOF >> result.html
	</tbody>
</table>
</body>
</html>
EOF


### mail sender
cat .mail_header result.html | sendmail -t
