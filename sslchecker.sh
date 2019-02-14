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

echo "=================================================================================================="
printf '| 도메인 %-30s\t | IP %-13s\t | 만료일 %-5s\t | 만료날짜 %-5s|\n'
echo "=================================================================================================="

for domainlist in $_DOMAINLIST
        do

        _today=`date +'%Y-%m-%d'`
        _VIP=`dig $domainlist +short`
        _ED=`./ssl-cert-info.sh --host $domainlist --end | awk {'print $1'}`
        _expire_date=`date -d "$_ED" +'%Y-%m-%d'`
        _expire_day=`dateDiff -d "$_today" "$_expire_date"`

        if [ $_expire_day -le 90 ] ; then  
                printf "| %-30s\t" "$domainlist"
                printf " | %-13s\t" "$_VIP"
                printf " | %-5d\t" "$_expire_day"
                printf " | %-5s\t |\n" "$_ED"
        fi

done

echo "=================================================================================================="

}

### call function
#sslchk
#sslchk > result.txt

### html
echo "<html>" > result.html
echo "<head>" >> result.html
echo "<meta http-equiv="Content-Type" content="text/html\; charset=utf-8" />" >> result.html
echo "</head>" >> result.html
echo "<body>" >> result.html
echo "<p>SSL 인증서 만료일 안내</p>" >> result.html
echo "<div style="width:100%\; overflow:auto"> " >> result.html
echo "<pre width="100%">" >> result.html
echo "<font face="Monaco">" >> result.html
sslchk >> result.html
echo "</font>" >> result.html
echo "</pre>" >> result.html
echo "</div>" >> result.html
echo "</body>" >> result.html
echo "</html>" >> result.html


### mail sender
#cat result.txt | mail -v -s "SSL 인증서 만료일 안내" anti1346@imicorp.co.kr
cat .mail_header result.html | sendmail -t

### call function && mail sender
#sslchk | mail -v -s "SSL 인증서 만료일 안내" anti1346@imicorp.co.kr

