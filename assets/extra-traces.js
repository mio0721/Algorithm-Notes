/* Character windows and insertion sort. Runs entirely offline. */
(()=>{
 const api=window.AlgorithmTraces,originalParse=api.parse,originalTrace=api.trace;
 api.defaults['1.7']={nums:[...'abcabcbbd']};
 api.defaults['1.8']={nums:[9,3,7,1,8,2,6,4,5]};
 api.parse=(id,raw,target)=>{
  if(id==='1.7'){
   if(/[^\x20-\x7e]/.test(raw))throw Error('本例与 C++ 字符代码对应，请输入英文、数字或英文标点。');
   if(raw.length>20)throw Error('演示最多接受 20 个字符。');return {arr:[...raw],value:null};
  }
  if(id==='1.8'){
   const text=raw.trim(),arr=text?text.split(/[,，\s]+/).map(Number):[];
   if(arr.length>20||arr.some(n=>!Number.isSafeInteger(n)||Math.abs(n)>1000000))throw Error('请输入最多 20 个整数，绝对值不超过 1000000。');
   return {arr,value:null};
  }
  return originalParse(id,raw,target);
 };
 api.trace=(id,arr,value)=>{
  if(!['1.7','1.8'].includes(id))return originalTrace(id,arr,value);
  const a=arr.slice(),frames=[];
  const add=(text,pointers={},range=null,active=[])=>frames.push({cells:a.map(String),text,pointers,range,active,indexed:true});
  if(id==='1.7'){
   const last=new Map();let left=0,best=0,bestStart=0;
   add('从空窗口开始；L 为左端，R 为当前新字符。');
   for(let right=0;right<a.length;right++){
    add(`读取字符 ${a[right]}，下标 ${right}。`,{L:left,R:right},[left,right],[right]);
    if(last.has(a[right])&&last.get(a[right])>=left){left=last.get(a[right])+1;add(`字符重复：左边界移到 ${left}，保持窗口无重复。`,{L:left,R:right},[left,right],[left,right]);}
    last.set(a[right],right);
    if(right-left+1>best){best=right-left+1;bestStart=left;}
    add(`当前窗口长度 ${right-left+1}；已知最长长度 ${best}。`,{L:left,R:right},[left,right]);
   }
   add(`完成：最长长度 ${best}，一个答案是「${a.slice(bestStart,bestStart+best).join('')}」。`,{},[bestStart,bestStart+best-1]);
  }else{
   add('插入排序：浅色部分是已排序前缀。',a.length?{i:0}:{},[0,0]);
   for(let i=1;i<a.length;i++){
    const key=a[i];let j=i-1;
    add(`取出待插入值 ${key}；左侧前 ${i} 项已有序。`,{i,j},[0,i-1],[i]);
    while(j>=0&&a[j]>key){
     add(`${a[j]} 大于 ${key}，准备右移。`,{i,j},[0,i-1],[j,j+1]);
     a[j+1]=a[j];add(`把 ${a[j]} 移到下标 ${j+1}；待插入值仍为 ${key}。`,{i,j},[0,i-1],[j+1]);j--;
    }
    a[j+1]=key;add(`把 ${key} 插到下标 ${j+1}，有序前缀扩展到 ${i}。`,{i},[0,i],[j+1]);
   }
   add(a.length?'排序完成：整个数组已有序。':'空数组已经有序。',{},[0,a.length-1]);
  }
  return frames;
 };
})();
