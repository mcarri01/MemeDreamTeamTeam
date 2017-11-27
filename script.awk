BEGIN {
    FS=""
}

FNR==NR { 
    if (length > max) {
        max = length
    }
    next
}

{
    while (length < max) {
        $0=$0 OFS
    }
    for (i=NF; i>=1; i--) {
        printf (i!=1) ? $i : $i ORS
    }
}
