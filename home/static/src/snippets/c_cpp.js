define("ace/snippets/c_cpp", ["require", "exports", "module"], function (t, n, e) {
    "use strict";
    n.snippetText = "## STL Collections\n# std::array\nsnippet array\n\tstd::array<${1:T}, ${2:N}> ${3};${4}\n" +
        "# vector\nsnippet vector\n\tvector<${1:T}> ${2};${3}\n" +
        "# deque\nsnippet deque\n\tdeque<${1:T}> ${2};${3}\n" +
        "# forward_list\nsnippet flist\n\tforward_list<${1:T}> ${2};${3}\n" +
        "# list\nsnippet list\n\tlist<${1:T}> ${2};${3}\n" +
        "# set\nsnippet set\n\tset<${1:T}> ${2};${3}\n" +
        "# map\nsnippet map\n\tmap<${1:Key}, ${2:T}> ${3};${4}\n" +
        "# multiset\nsnippet mset\n\tmultiset<${1:T}> ${2};${3}\n" +
        "# multimap\nsnippet mmap\n\tmultimap<${1:Key}, ${2:T}> ${3};${4}\n" +
        "# unordered_set\nsnippet uset\n\tunordered_set<${1:T}> ${2};${3}\n" +
        "# unordered_map\nsnippet umap\n\tunordered_map<${1:Key}, ${2:T}> ${3};${4}\n" +
        "# unordered_multiset\nsnippet umset\n\tunordered_multiset<${1:T}> ${2};${3}\n" +
        "# unordered_multimap\nsnippet ummap\n\tunordered_multimap<${1:Key}, ${2:T}> ${3};${4}\n" +
        "# stack\nsnippet stack\n\tstack<${1:T}> ${2};${3}\n" +
        "# queue\nsnippet queue\n\tqueue<${1:T}> ${2};${3}\n" +
        "# priority_queue\nsnippet pqueue\n\tpriority_queue<${1:T}> ${2};${3}\n##\n## Access Modifiers\n" +
        "# class\nsnippet cl\n\tclass ${1:`Filename('$1', 'name')`} \n\t{\n\tpublic:\n\t\t$1(${2});\n\t\t~$1();\n\n\tprivate:\n\t\t${3:/* data */}\n\t};\n" +
        "# member function implementation\nsnippet mfun\n\t${4:void} ${1:`Filename('$1', 'ClassName')`}::${2:memberFunction}(${3}) {\n\t\t${5:/* code */}\n\t}\n" +
        "# cout\nsnippet cout\n\tcout << ${1} << endl;${2}\n" +
        "# cin\nsnippet cin\n\tcin >> ${1};${2}\n##\n## Iteration\n" +
        "# for i \nsnippet fori\n\tfor (int ${2:i} = 0; $2 < ${1:count}; $2${3:++}) {\n\t\t${4:/* code */}\n\t}${5}\n\n" +
        "# foreach\nsnippet fore\n\tfor (${1:auto} ${2:i} : ${3:container}) {\n\t\t${4:/* code */}\n\t}${5}\n" +
        "# iterator\nsnippet iter\n\tfor (${1:vector}<${2:type}>::${3:const_iterator} ${4:i} = ${5:container}.begin(); $4 != $5.end(); ++$4) {\n\t\t${6}\n\t}${7}\n\n" +
        "# auto iterator\nsnippet itera\n\tfor (auto ${1:i} = $1.begin(); $1 != $1.end(); ++$1) {\n\t\t${2:cout << *$1 << endl;}\n\t}${3}\n##\n## Lambdas\n" +
        "# printf\nsnippet printf\n\tprintf(\"${1:}${2};${3}\n" +
        "# scanf\nsnippet scanf\n\tscanf(\"${1:}${2};${3}\n" +
        "# include\nsnippet include\n\tinclude<${1:} ${2}${3}\n" +
        "# stdio.h\nsnippet stdio.h\n\tstdio.h>${1:}${2}${3}\n" +
        "# iostream\nsnippet iostream\n\tiostream>${1:}${2}${3}\n" +
        "# vector\nsnippet vector\n\tvector>${1:}${2}${3}\n" +
        "# math.h\nsnippet math.h\n\tmath.h${1:}${2}${3}\n" +
        "# bits\\stdc++.h\nsnippet bits\\stdc++.h\n\tbits\\stdc++.h>${1:}${2}${3}\n" +
        "# main\nsnippet main\n\tmain(){${1:}} ${2}${3}${4}\n" +
        "# lambda (multi-line)\nsnippet lld\n\t[${1}](${2}){\n\t\t${3:/* code */}\n\t}${4}\n", n.scope = "c_cpp"

}), window.require(["ace/snippets/c_cpp"], function (t) {
    "object" == typeof module && "object" == typeof exports && module && (module.exports = t)
});