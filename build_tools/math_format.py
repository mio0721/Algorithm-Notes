"""Typeset prose only. Code, JSON, form values and animation messages stay literal."""
import re
from html import escape
from html.parser import HTMLParser

DISPLAY = {
'4.1': r'\text{选择}\;\longrightarrow\;\text{递归探索}\;\longrightarrow\;\text{撤销选择}',
'4.2': r's_i\ge e_{\mathrm{last}}\quad\Longrightarrow\quad e_{\mathrm{last}}\gets e_i',
'4.3': r'T(n)=2T\!\left(\frac n2\right)+\Theta(n)=\Theta(n\log n)',
'4.4': r'\begin{aligned}d_0&=1,\qquad d_1=1,\\d_i&=d_{i-1}+d_{i-2}\quad(i\ge2).\end{aligned}',
'4.5': r'\begin{aligned}D_{i,c}&=\max\left(D_{i-1,c},D_{i-1,c-w_i}+v_i\right)\quad(c\ge w_i),\\d_c&\gets\max(d_c,d_{c-w_i}+v_i),\quad c=C,C-1,\ldots,w_i.\end{aligned}',
'4.6': r'D_{i,j}=\begin{cases}D_{i-1,j-1}+1,&a_{i-1}=b_{j-1},\\\max(D_{i-1,j},D_{i,j-1}),&a_{i-1}\ne b_{j-1}.\end{cases}',
'5.1': r'\text{连通分量数}=\text{从未访问顶点发起完整搜索的次数}',
'5.2': r'd_v\gets\min\bigl(d_v,d_u+w(u,v)\bigr)',
'5.3': r'\begin{aligned}f(u)&=g(u)+h(u),\\h(u)&=|r_u-r_T|+|c_u-c_T|.\end{aligned}',
'5.4': r'D^{(k)}_{i,j}=\min\!\left(D^{(k-1)}_{i,j},D^{(k-1)}_{i,k}+D^{(k-1)}_{k,j}\right)',
'5.5': r'\operatorname{indegree}(v)\gets\operatorname{indegree}(v)-1;\qquad\operatorname{indegree}(v)=0\Longrightarrow v\text{ 入队}',
'5.6': r'r_a=\operatorname{find}(a),\quad r_b=\operatorname{find}(b);\qquad r_a\ne r_b\Longrightarrow\text{合并两棵集合树}',
'5.7': r'\operatorname{find}(u)\ne\operatorname{find}(v)\Longrightarrow\text{选边并合并};\qquad |T|=|V|-1\quad\text{（连通图）}',
'6.1': r'\begin{aligned}L&=\Delta\cdot N_{\mathrm{steps}},\\N_{\mathrm{inflate}}&=\left\lceil\frac{r_{\mathrm{robot}}}{\Delta}\right\rceil.\end{aligned}',
'6.2': r'\begin{aligned}\operatorname{rhs}(t)&=0,\\\operatorname{rhs}(u)&=\min_{v\in\operatorname{Succ}(u)}\bigl[c(u,v)+g(v)\bigr],\\u\text{ 一致}&\iff g(u)=\operatorname{rhs}(u).\end{aligned}',
'6.3': r'q_{\mathrm{new}}=q_{\mathrm{near}}+\min\!\left(1,\frac{\eta}{\|q_{\mathrm{rand}}-q_{\mathrm{near}}\|}\right)(q_{\mathrm{rand}}-q_{\mathrm{near}})',
'6.4': r'\operatorname{parent}(q)=\underset{v\in\mathcal N_{\mathrm{free}}(q)}{\arg\min}\;\bigl[\operatorname{cost}(v)+\|v-q\|\bigr]',
'6.5': r'\begin{aligned}\tau&=\frac tT,\qquad s(t)=D(10\tau^3-15\tau^4+6\tau^5),\\v(t)&=\frac DT(30\tau^2-60\tau^3+30\tau^4),\\a(t)&=\frac D{T^2}(60\tau-180\tau^2+120\tau^3).\end{aligned}',
}

SPECIAL = {
'r=min(2.5,9√(log(n+1)/(n+1)))':r'r=\min\!\left(2.5,9\sqrt{\frac{\log(n+1)}{n+1}}\right)',
'T(n)=2T(n/2)+O(n)':r'T(n)=2T(n/2)+O(n)',
'3n²+5n+2':r'3n^2+5n+2',
'dp[i]=dp[i−1]+dp[i−2]':r'\mathrm{dp}_i=\mathrm{dp}_{i-1}+\mathrm{dp}_{i-2}',
'dp[c]=max(dp[c],dp[c−w]+v)':r'\mathrm{dp}_c=\max(\mathrm{dp}_c,\mathrm{dp}_{c-w}+v)',
'h=|r−rT|+|c−cT|':r'h=|r-r_T|+|c-c_T|',
'f=g+h':r'f=g+h',
'h(u)≤cost(u,v)+h(v)':r'h(u)\le\operatorname{cost}(u,v)+h(v)',
'rhs(goal)=0':r'\operatorname{rhs}(\mathrm{goal})=0',
'rhs(u)=min[c(u,v)+g(v)]':r'\operatorname{rhs}(u)=\min_v[c(u,v)+g(v)]',
'g≠rhs':r'g\ne\operatorname{rhs}',
'g(u)=rhs(u)':r'g(u)=\operatorname{rhs}(u)',
'g>rhs':r'g>\operatorname{rhs}',
'g≤rhs':r'g\le\operatorname{rhs}',
'cost[v]=cost[parent[v]]+边长':r'\operatorname{cost}(v)=\operatorname{cost}(\operatorname{parent}(v))+\ell(\operatorname{parent}(v),v)',
's(t)=D(10τ³−15τ⁴+6τ⁵)':r's(t)=D(10\tau^3-15\tau^4+6\tau^5)',
'τ=t/T':r'\tau=t/T',
'(15/8)|D|/T':r'\frac{15|D|}{8T}',
'(10√3/3)|D|/T²':r'\frac{10\sqrt3\,|D|}{3T^2}',
'q′(s)·ṡ':r'q^{\prime}(s)\dot s',
'q″(s)ṡ²+q′(s)s̈':r'q^{\prime\prime}(s)\dot s^2+q^{\prime}(s)\ddot s',
'v²κ':r'v^2\kappa',
'1/T²':r'1/T^2',
'1/T':r'1/T',
'1/2':r'\frac12',
'10√3/3':r'\frac{10\sqrt3}{3}',
'vmax=2':r'v_{\max}=2',
'amax=1':r'a_{\max}=1',
}
SPECIAL_RE=re.compile('|'.join(re.escape(s) for s in sorted(SPECIAL,key=len,reverse=True)))

def tex(expression):
    expression=expression.replace('字符集大小',r'|\Sigma|')
    for a,b in [('²','^2'),('³','^3'),('⁴','^4'),('ⁿ','^n'),('·',r'\cdot '),('×',r'\times '),('−','-'),('α',r'\alpha '),('∞',r'\infty')]:
        expression=expression.replace(a,b)
    expression=re.sub(r'\b(log|min|max)\b',lambda m:'\\'+m[0]+' ',expression)
    return expression

def inline(value):
    cls='math-inline math-long' if len(value)>65 else 'math-inline'
    return '<span class="'+cls+'">$'+escape(value)+'$</span>'

def text_math(text):
    # Tokenize first: replacements must not be fed back through this function.
    pattern=re.compile(r'O\(|'+SPECIAL_RE.pattern+r'|\bdp(?:\[[^\]\n]+\]){1,2}|\b(?:rhs|g|h|f|cost)\((?:u|v|start|goal|n)\)|\b(?:n|V|N|T|2)[²³ⁿ]|\blog n\b')
    result=[];position=0
    while True:
        match=pattern.search(text,position)
        if not match:result.append(escape(text[position:]));break
        result.append(escape(text[position:match.start()]))
        token=match[0];end=match.end()
        if token=='O(':
            depth=1
            while end<len(text) and depth:
                if text[end]=='(':depth+=1
                if text[end]==')':depth-=1
                end+=1
            if depth or end-match.start()>120:
                result.append(escape(token));position=match.end();continue
            token=text[match.start():end]
            rendered=tex(token)
        elif token in SPECIAL:rendered=SPECIAL[token]
        elif token.startswith('dp['):
            indices=re.findall(r'\[([^]]+)\]',token)
            rendered=r'\mathrm{dp}_{'+','.join(tex(x) for x in indices)+'}'
        elif token.startswith(('rhs(','cost(')):
            name,args=token.split('(',1)
            rendered='\\operatorname{'+name+'}('+args
        else:rendered=tex(token)
        result.append(inline(rendered));position=end
    return ''.join(result)

class Formatter(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.output=[];self.stack=[]
    def handle_starttag(self,tag,attrs):
        self.output.append(self.get_starttag_text())
        if tag not in ('br','hr','img','input','meta','link','source','wbr'):
            skip=tag in ('code','pre','script','style','textarea') or bool(self.stack and self.stack[-1][1])
            # Already-authored MathJax text stays untouched.
            if any(name=='class' and 'math-' in value for name,value in attrs if value):skip=True
            self.stack.append((tag,skip))
    def handle_startendtag(self,tag,attrs):self.output.append(self.get_starttag_text())
    def handle_endtag(self,tag):
        self.output.append('</'+tag+'>')
        if self.stack and self.stack[-1][0]==tag:self.stack.pop()
    def handle_data(self,data):
        self.output.append(data if self.stack and self.stack[-1][1] else text_math(data))
    def handle_entityref(self,name):self.output.append('&'+name+';')
    def handle_charref(self,name):self.output.append('&#'+name+';')
    def handle_comment(self,data):self.output.append('<!--'+data+'-->')

def mathify(html):
    parser=Formatter();parser.feed(html);return ''.join(parser.output)

def display(id):
    return '<div class="math-display">$$\n'+escape(DISPLAY[id])+'\n$$</div>'
