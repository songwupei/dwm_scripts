#!/bin/zsh
## source by ~/.zshrc
## 11.pandoc convert
mdstodocxs(){
		for name ($(fd -e ${${1:t}:e} ${${1:t}:r} ${1:h}) ){
			mdtodocx $name
	}
}
mdtodocx() {
		# base the reference-doc 
		# pandoc md to docx
	fname=$1
	ofile=${fname:h}/${${fname:t}:r}_md.docx
	pandoc -s ${fname} -o $ofile --reference-doc=/home/song/NutstoreFiles/0-Notes/1-MyNormals/normal.dotx
	unset fname
	echo "convert $1 to ${${1:t}:r}.dotx"
}

docxstomds(){
		for name ($(fd -e ${${1:t}:e} ${${1:t}:r} ${1:h}) ){
			   docxtomd $name
	}
}

docxtomd() {
		# base the reference-doc 
		# pandoc md to docx
	# fname=$(fd $1 -e docx) #if has extend  -e docx)
	fname=$1
	echo "convert docx to markdown"
	pandoc  -s ${fname} -f docx -t markdown -o "${fname:r}.md" 
	unset fname
	echo "convert $1 to ${1:r}.md"
}

formatmds() {
		for name ($(fd -e ${${1:t}:e} ${${1:t}:r} ${1:h}) ){
			   formatmd $name $2
}
}

formatmd() {
	hanznum=一二三四五六七八九十
	(($+2)) && {
	case $2 {
		(basic)
		#sed -e 's/\([一二三四五六七八九十]、\)/## \1/' -e '1s/^/# /' -e 's/\(（\([一二三四五六七八九]\)）\)/### \1/' -e 's/\(^附件1\)/<br>\n\n<br\/>\n\n\1/' $1 > "${1:r}_format.${1:e}"
		sed -e 's/\([一二三四五六七八九十]、\)/## \1/' -e '1s/^/# /' -e 's/\(（\([一二三四五六七八九]\)）\)/### \1/' -e 's/\(^附件1\)/\n\n<br>\n\n\1/' $1 > "${1:r}_format.${1:e}"
		;;
	(inline)
		# replacehznum 解决sed 的贪婪模式， [^str]可以截断
		tmpmd=${1:r}_tmp.${1:e}

		replacehznum $1 > ${tmpmd}
	        sed -e 's/\([一二三四五六七八九十]、\)/## \1/' -e '1s/^/# /' -e 's/\(（\([一二三四五六七八九]\)）\)/### \1/' -e 's/\(^附件1\)/\n\n<br>\n\n\1/' ${tmpmd} > "${1:r}_format.${1:e}"
		rm ${tmpmd}
		;;
####	(skBold)
####		# 暂时无法解决sed 的贪婪模式，需要使用202去截断
####		# 网上说 perl -pe [^str]可以截断， TODO
####		sed -e 's/\([一二三四五六]、\)/## \1/' -e '1s/^/# /' -e 's/\(（[一二三四五六七八九十]）.*。\)\(202\)/**\1**\2/' $1  -e 's/\(^附件1\)/<br\/>\n\r\n\r\1/'> "${1:r}_format.${1:e}"
####		;;
	(*)
	echo 	err
		;;
	}
}
echo 'format $1 ;then convert to docx'
	echo "format $1 to ${1:r}_format.${1:e}"
}

replacehznum() {
	# 删除tmp文件夹
	formatmdTemp="/tmp/formatmdTemp"
	formatmdCmd="$formatmdTemp/formatmdCmd"

	[[ -e $formatmdTemp ]] && rm -rf $formatmdTemp 
        mkdir $formatmdTemp
	# nl -ba ==include blank lines
	nl -ba $1 | grep （[一二三四五六七八九]）| cut -f 1 | tr -d '\n' > $formatmdTemp/linesnumber
	# nls=$(nl $1 | grep （[一二三四]）| cut -f 1 | tr -d '\n')
nls=($(cat $formatmdTemp/linesnumber))
txt=$(cat $1)
hanznum="一二三四五六七八九十"
printf "sed " > $formatmdCmd
for lnum ($nls) { 
hzindex=${nls[(ie)$lnum]}
## case1:1-only format Heading3 （一）xx。regex not greed :use [^str] 
## case1:2-replace (一) (三) to(一) (二) 
### printf " -e '%s s/（[一二三四五六七八九]）\([^。]*。\)/（%s）\\%s/' %s" ${lnum} ${hanznum[$hzindex]} 1  >> $formatmdCmd
## case2:case1 + second format NormalCharacter<span>***</span>
printf " -e '%s s/（[一二三四五六七八九]）\([^。]*。\)\(.*。\)/（%s）\\%s<span custom-style="NormalCharacter">\\%s<\/span>/' %s" ${lnum} ${hanznum[$hzindex]} 1 2  >> $formatmdCmd
}
printf "%s" $1 >> $formatmdCmd
zsh $formatmdCmd 

}
