/* Step traces for the six array lessons. Input and animations run locally. */
(()=>{
'use strict';
const defaults={
 '1.1':{nums:[-5,-1,0,3,5,9,12,16,20],value:9},'1.2':{nums:[1,3,5,6,8,10,12,15,18],value:7},
 '1.3':{nums:[1,2,4,6,9,12,15,19,23],value:17},'1.4':{nums:[0,0,1,1,2,2,3,3,4],value:null},
 '1.5':{nums:[3,2,2,3,4,3,5,2,3],value:3},'1.6':{nums:[2,3,1,2,4,3,1,2,5],value:7}
};
function format(a){return a.map(String)}
function trace(id,nums,value){
 const a=nums.slice(),frames=[],n=a.length;
 const add=(text,active=[],pointers={},range=null)=>frames.push({cells:format(a),text,active,indexed:true,pointers,range});
 if(id==='1.1'){
  let l=0,r=n-1;add(`目标 ${value}；初始闭区间 [${l}, ${r}]。`,[],{L:l,R:r},[l,r]);
  while(l<=r){const m=l+Math.floor((r-l)/2);add(`left=${l}，right=${r}，mid=${m}，中点值 ${a[m]}。`,[m],{L:l,M:m,R:r},[l,r]);if(a[m]===value){add(`找到目标，返回下标 ${m}。`,[m],{L:l,M:m,R:r},[l,r]);return frames}if(a[m]<value){l=m+1;add(`中点值小于目标，令 left=${l}，排除左半部分。`,[],{L:l,R:r},[l,r])}else{r=m-1;add(`中点值大于目标，令 right=${r}，排除右半部分。`,[],{L:l,R:r},[l,r])}}
  add('候选区间为空，没有找到目标，返回 -1。',[],{L:l,R:r},[l,r]);
 }else if(id==='1.2'){
  let l=0,r=n;add(`目标 ${value}；初始左闭右开区间 [${l}, ${r})。`,[],{L:l,'R(开)':r},[l,r-1]);
  while(l<r){const m=l+Math.floor((r-l)/2);add(`left=${l}，right=${r}，mid=${m}，中点值 ${a[m]}。`,[m],{L:l,M:m,'R(开)':r},[l,r-1]);if(a[m]<value){l=m+1;add(`中点值小于目标，令 left=${l}。`,[],{L:l,'R(开)':r},[l,r-1])}else{r=m;add(`中点值不小于目标，保留它作为边界：right=${r}。`,[],{L:l,'R(开)':r},[l,r-1])}}
  add(`边界位置为 ${l}；可在此处插入，或该位置已是第一个等于目标的元素。`,l<n?[l]:[],{L:l,'R(开)':r},null);
 }else if(id==='1.3'){
  let l=0,r=n-1;add(`目标和 ${value}；左右指针从两端开始。`,[],{L:l,R:r},[l,r]);
  while(l<r){const sum=a[l]+a[r];add(`${a[l]} + ${a[r]} = ${sum}，left=${l}，right=${r}。`,[l,r],{L:l,R:r},[l,r]);if(sum===value){add(`找到结果：从 1 开始的下标 [${l+1}, ${r+1}]。`,[l,r],{L:l,R:r},[l,r]);return frames}if(sum<value){l++;add(`和太小，左指针右移至 ${l}。`,[],{L:l,R:r},[l,r])}else{r--;add(`和太大，右指针左移至 ${r}。`,[],{L:l,R:r},[l,r])}}
  add('左右指针相遇，没有找到满足条件的两个元素。',[],{L:l,R:r},null);
 }else if(id==='1.4'){
  if(!n){add('输入为空，返回长度 0。');return frames}
  let slow=0;add('先保留第一个元素；slow 指向有效前缀最后一项。',[0],{slow:0},[0,0]);
  for(let fast=1;fast<n;fast++){
   add(`fast=${fast}，比较 ${a[fast]} 与 nums[slow]=${a[slow]}。`,[slow,fast],{slow,fast},[0,slow]);
   if(a[fast]!==a[slow]){slow++;a[slow]=a[fast];add(`发现新值，slow=${slow}，写入 ${a[slow]}。`,[slow,fast],{slow,fast},[0,slow])}else add('值重复，slow 不动，继续扫描。',[slow,fast],{slow,fast},[0,slow]);
  }
  add(`返回长度 ${slow+1}；有效前缀为 [${a.slice(0,slow+1).join(', ')}]。`,Array.from({length:slow+1},(_,i)=>i),{slow},[0,slow]);
 }else if(id==='1.5'){
  let slow=0;add(`移除 ${value}；slow 表示下一个写入位置。`,[],{slow},null);
  for(let fast=0;fast<n;fast++){
   if(a[fast]!==value){const x=a[fast];a[slow]=x;add(`fast=${fast}，保留 ${x} 并写到位置 ${slow}，然后 slow 前进。`,[slow,fast],{slow,fast},[0,slow]);slow++;add(`写入完成，下一个写入位置 slow=${slow}。`,[],{slow,fast},[0,slow-1])}else add(`fast=${fast}，值为 ${value}，跳过，slow=${slow}。`,[fast],{slow,fast},[0,slow-1]);
  }
  add(`返回长度 ${slow}；有效前缀为 [${a.slice(0,slow).join(', ')}]。`,Array.from({length:slow},(_,i)=>i),{slow},[0,slow-1]);
 }else if(id==='1.6'){
  let l=0,sum=0,best=Infinity;add(`目标和 ${value}；所有元素为正，开始扩展窗口。`,[],{L:0},null);
  for(let r=0;r<n;r++){
   sum+=a[r];add(`加入下标 ${r} 的 ${a[r]}，窗口 [${l}, ${r}]，和为 ${sum}。`,[r],{L:l,R:r},[l,r]);
   while(sum>=value){best=Math.min(best,r-l+1);add(`和 ${sum} 达标，记录当前最短长度 ${best}。`,[],{L:l,R:r},[l,r]);sum-=a[l];l++;add(`移走左端，left=${l}，窗口和为 ${sum}。`,[],{L:l,R:r},[l,r])}
  }
  add(`扫描结束，返回 ${best===Infinity?0:best}。${best===Infinity?'没有满足条件的连续子数组。':''}`);
 }
 return frames;
}
function parse(id,raw,v){
 const trimmed=raw.trim();let arr=[];
 if(trimmed){let fields=trimmed.split(/[,，\s]+/);if(fields.length>20)throw Error('演示最多输入 20 个整数。');if(fields.some(x=>!/^[-+]?\d+$/.test(x)))throw Error('数组请用逗号或空格分隔整数。');arr=fields.map(Number);if(arr.some(x=>!Number.isSafeInteger(x)||Math.abs(x)>1000000))throw Error('请输入绝对值不超过 1000000 的安全整数。')}
 if(['1.1','1.2','1.3','1.4'].includes(id)&&arr.some((x,i)=>i>0&&x<arr[i-1]))throw Error('本算法要求数组按非递减顺序排列。');
 if(id==='1.6'&&arr.some(x=>x<=0))throw Error('本滑动窗口算法要求数组元素均为正整数。');
 let value=null;if(id!=='1.4'){if(!/^[-+]?\d+$/.test(v.trim()))throw Error('目标值请填写整数。');value=Number(v);if(!Number.isSafeInteger(value)||Math.abs(value)>1000000)throw Error('目标值的绝对值不能超过 1000000。');if(id==='1.6'&&value<=0)throw Error('最小子数组的目标值必须大于 0。')}
 return {arr,value};
}
window.AlgorithmTraces={defaults,trace,parse};
})();
