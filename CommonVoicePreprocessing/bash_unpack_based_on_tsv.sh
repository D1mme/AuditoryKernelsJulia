array_abcdef=("ab" "af" "am" "ar" "as" "ast" "az" "ba" "bas" "be" "bg" "bn" "br" "ca" "ckb" "cnh" "cs" "cv" "cy" "da" "dav" "de" "dv" "dyu" "el" "en" "eo" "es" "et" "eu" "fa" "fi" "fr" "fy-NL")
array_ghijkl=("ga-IE" "gl" "gn" "ha" "he" "hi" "hsb" "ht" "hu" "hy-AM" "ia" "id" "ig" "is" "it" "ja" "ka" "kab" "kk" "kln" "kmr" "ko" "ky" "lg" "lij" "lo" "lt" "ltg" "luo" "lv")
array_mnopqr=("mdf" "mhr" "mk" "ml" "mn" "mr" "mrj" "mt" "myv" "nan-tw" "ne-NP" "nhi" "nl" "nn-NO" "nr" "nso" "oc" "or" "os" "pa-IN" "pl" "ps" "pt" "quy" "rm-sursilv" "rm-vallader" "ro" "ru" "rw")
array_stuvwxyz=("sah" "sat" "sc" "sd" "sk" "skr" "sl" "sq" "sr" "st" "sv-SE" "sw" "ta" "te" "th" "ti" "tig" "tk" "tn" "tok" "tr" "ts" "tt" "tw" "ug" "uk" "ur" "uz" "vi" "vot" "xh" "yi" "yo" "yue" "zgh" "zh-CN" "zh-HK" "zh-TW" "zu" "zza")

array_abcdef_valid=("ab" "ar" "ba" "bas" "be" "bg" "bn" "br" "ca" "ckb" "cs" "cy" "da" "dav" "de" "dv" "el" "en" "eo" "es" "et" "eu" "fa" "fi" "fr" "fy-NL")
array_ghijkl_valid=("gl" "ha" "hi" "hu" "hy-AM" "ia" "id" "it" "ja" "ka" "kab" "kln" "kmr" "ky" "lg" "lt" "ltg" "luo" "lv")
array_mnopqr_valid=("mhr" "mk" "mn" "mr" "mrj" "mt" "nan-tw" "nl" "or" "pl" "ps" "pt" "rm-sursilv" "ro" "ru" "rw")
array_stuvwxyz_valid=("sah" "sk" "sq" "sv-SE" "sw" "ta" "th" "tok" "tr" "tt" "ug" "uk" "ur" "uz" "vi" "yo" "yue" "zh-CN" "zh-HK" "zh-TW")

echo "Total numbers"
echo "Number of elements: ${#array_abcdef[@]}"
echo "Number of elements: ${#array_ghijkl[@]}"
echo "Number of elements: ${#array_mnopqr[@]}"
echo "Number of elements: ${#array_stuvwxyz[@]}"

echo "Total valid numbers"
echo "Number of elements: ${#array_abcdef_valid[@]}"
echo "Number of elements: ${#array_ghijkl_valid[@]}"
echo "Number of elements: ${#array_mnopqr_valid[@]}"
echo "Number of elements: ${#array_stuvwxyz_valid[@]}"

for element in "${array_abcdef_valid[@]}"
do
    echo "$element"
	python unpack_cv_based_on_TSV.py --id "$element" --tsv train_m_short.tsv
done
