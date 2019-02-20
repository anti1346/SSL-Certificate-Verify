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
    _ToDay=`date +'%Y-%m-%d'`
    _IP_Address=`dig $domainlist +short | paste -sd ", "`
    _Expired_Date=`./ssl-cert-info.sh --host $domainlist --end | awk {'print $1'}`
    _Expiration_Date=`date -d "$_Expired_Date" +'%Y-%m-%d'`
    _Expired_Days=`dateDiff -d "$_ToDay" "$_Expiration_Date"`

    if [ $_Expired_Days -lt 30 ] ; then
     	printf "<tr><td>Must update 30 days ago</td><td>$domainlist</td><td>$_IP_Address</td><td>$_Expired_Days</td><td>$_Expired_Date</td></tr>\n" "$domainlist" "$_IP_Address" "$_Expired_Days" "$_Expired_Date"
    elif [ $_Expired_Days -gt 30 -a $_Expired_Days -le 90 ] ; then
	printf "<tr><td>Must update 30 to 90 days ago</td><td>$domainlist</td><td>$_IP_Address</td><td>$_Expired_Days</td><td>$_Expired_Date</td></tr>\n" "$domainlist" "$_IP_Address" "$_Expired_Days" "$_Expired_Date"
    else
	printf "<tr><td>OK</td><td>$domainlist</td><td>$_IP_Address</td><td>$_Expired_Days</td><td>$_Expired_Date</td></tr>\n" "$domainlist" "$_IP_Address" "$_Expired_Days" "$_Expired_Date"
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
<style>
  table {
    width: 80%;
    border-top: 1px solid #444444;
    border-collapse: collapse;
    font-family: Monaco;
    font-size:90%;
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
    background-color: #FFFFFF;
  }
</style>
</head>
<body>
<font face="Monaco">
<table border="1px">
	<thead>
		<tr><th>Condition</th><th>Domain</th><th>IP Address</th><th>Expired Days</th><th>Expiration Date</th></tr>
	</thead>
	<tbody>
EOF

sslchk >> result.html

cat <<EOF >> result.html
	</tbody>
</table>
</font>
</body>
</html>
EOF

### mail sender
cat .mail_header result.html | sendmail -t
