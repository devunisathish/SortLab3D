from flask import Flask, render_template, request, jsonify
import subprocess, tempfile, os, json, shutil
app=Flask(__name__)
ALG={
'bubble':('Bubble Sort','O(n^2)','O(1)','for(int i=0;i<n-1;i++){for(int j=0;j<n-i-1;j++){TRACE(3,i,j,-1,"compare");if(a[j]>a[j+1]){int t=a[j];a[j]=a[j+1];a[j+1]=t;swaps++;TRACE(7,i,j,t,"swap");}}TRACE(9,i,-1,-1,"pass");}'),
'selection':('Selection Sort','O(n^2)','O(1)','for(int i=0;i<n-1;i++){int m=i;for(int j=i+1;j<n;j++){TRACE(3,i,j,m,"compare");if(a[j]<a[m])m=j;}if(m!=i){int t=a[i];a[i]=a[m];a[m]=t;swaps++;TRACE(8,i,m,t,"swap");}TRACE(9,i,-1,m,"pass");}'),
'insertion':('Insertion Sort','O(n^2)','O(1)','for(int i=1;i<n;i++){int key=a[i],j=i-1;while(j>=0&&a[j]>key){TRACE(3,i,j,key,"compare");a[j+1]=a[j];shifts++;j--;TRACE(6,i,j,key,"shift");}a[j+1]=key;TRACE(8,i,j+1,key,"insert");}'),
'quick':('Quick Sort','Average O(n log n), worst O(n^2)','O(log n)','void qs(int a[],int l,int h){if(l<h){int p=a[h],i=l-1;for(int j=l;j<h;j++){TRACE(3,i,j,p,"compare");if(a[j]<p){i++;int t=a[i];a[i]=a[j];a[j]=t;if(i!=j)swaps++;TRACE(6,i,j,p,"partition-swap");}}int t=a[i+1];a[i+1]=a[h];a[h]=t;swaps++;TRACE(9,i+1,h,p,"pivot");qs(a,l,i);qs(a,i+2,h);}}\nqs(a,0,n-1);'),
'merge':('Merge Sort','O(n log n)','O(n)','void mg(int a[],int l,int m,int r){int L[256],R[256],x=m-l+1,y=r-m;for(int i=0;i<x;i++)L[i]=a[l+i];for(int j=0;j<y;j++)R[j]=a[m+1+j];int i=0,j=0,k=l;while(i<x&&j<y){TRACE(7,i,j,k,"compare");a[k++]=(L[i]<=R[j])?L[i++]:R[j++];writes++;TRACE(8,i,j,k-1,"write");}while(i<x){a[k++]=L[i++];writes++;TRACE(10,i,j,k-1,"write");}while(j<y){a[k++]=R[j++];writes++;TRACE(11,i,j,k-1,"write");}}\nvoid ms(int a[],int l,int r){if(l<r){int m=(l+r)/2;TRACE(14,l,r,m,"divide");ms(a,l,m);ms(a,m+1,r);mg(a,l,m,r);}}\nms(a,0,n-1);'),
'heap':('Heap Sort','O(n log n)','O(1)','void hp(int a[],int n,int i){int m=i,l=2*i+1,r=2*i+2;if(l<n&&a[l]>a[m])m=l;if(r<n&&a[r]>a[m])m=r;TRACE(4,i,m,n,"compare");if(m!=i){int t=a[i];a[i]=a[m];a[m]=t;swaps++;TRACE(7,i,m,t,"swap");hp(a,n,m);}}\nfor(int i=n/2-1;i>=0;i--)hp(a,n,i);for(int i=n-1;i>0;i--){int t=a[0];a[0]=a[i];a[i]=t;swaps++;TRACE(11,0,i,t,"extract");hp(a,i,0);}'),
'counting':('Counting Sort','O(n + k)','O(k)','int c[100]={0},o[256];for(int i=0;i<n;i++){c[a[i]]++;TRACE(2,i,-1,a[i],"count");}for(int i=1;i<100;i++)c[i]+=c[i-1];for(int i=n-1;i>=0;i--){o[--c[a[i]]]=a[i];TRACE(5,i,c[a[i]],a[i],"place");}for(int i=0;i<n;i++){a[i]=o[i];writes++;TRACE(6,i,-1,a[i],"write");}'),
'radix':('Radix Sort','O(d(n + 10))','O(n + 10)','int max=a[0],o[256];for(int i=1;i<n;i++)if(a[i]>max)max=a[i];for(int e=1;max/e>0;e*=10){int c[10]={0};for(int i=0;i<n;i++){c[(a[i]/e)%10]++;TRACE(3,i,-1,e,"digit-count");}for(int i=1;i<10;i++)c[i]+=c[i-1];for(int i=n-1;i>=0;i--){int d=(a[i]/e)%10;o[--c[d]]=a[i];TRACE(7,i,d,e,"digit-place");}for(int i=0;i<n;i++){a[i]=o[i];writes++;TRACE(8,i,-1,e,"digit-write");}}')
}
def source(key,arr):
    body=ALG[key][3]
    if key in ('quick','merge','heap'):
        parts=body.split('\n')
        funcs='\n'.join(parts[:-1]); call=parts[-1]
    else: funcs=''; call=body
    vals=','.join(map(str,arr))
    return '''#include <stdio.h>
int swaps=0,writes=0,shifts=0,comparisons=0,n,A[256];
void tr(int line,int x,int y,int z,const char *ev){if(ev[0]=='c')comparisons++;printf("{\\\"line\\\":%d,\\\"x\\\":%d,\\\"y\\\":%d,\\\"z\\\":%d,\\\"event\\\":\\\"%s\\\",\\\"array\\\":[",line,x,y,z,ev);for(int i=0;i<n;i++){if(i)printf(",");printf("%d",A[i]);}printf("],\\\"comparisons\\\":%d,\\\"swaps\\\":%d,\\\"writes\\\":%d,\\\"shifts\\\":%d}\\n",comparisons,swaps,writes,shifts);}
#define TRACE(L,X,Y,Z,E) tr(L,X,Y,Z,E)
''' + funcs + '\nint main(){int init['+str(len(arr))+']={'+vals+'};n='+str(len(arr))+';for(int i=0;i<n;i++)A[i]=init[i];int *a=A;tr(0,-1,-1,-1,"start");'+call+'tr(999,-1,-1,-1,"done");return 0;}'

DISPLAY={
"bubble":"void sort(int a[], int n) {\n    for (int i = 0; i < n - 1; i++) {\n        for (int j = 0; j < n - i - 1; j++) {\n            TRACE(3, i, j, -1, \"compare\");\n            if (a[j] > a[j+1]) {\n                swap(a[j], a[j+1]);\n                TRACE(7, i, j, -1, \"swap\");\n            }\n        }\n        TRACE(9, i, -1, -1, \"pass\");\n    }\n}",
"selection":"void sort(int a[], int n) {\n    for (int i = 0; i < n-1; i++) {\n        for (int j = i+1; j < n; j++) {\n            TRACE(3, i, j, min_idx, \"compare\");\n            if (a[j] < a[min_idx]) min_idx = j;\n        }\n        if (min_idx != i) {\n            swap(a[i], a[min_idx]);\n            TRACE(8, i, min_idx, -1, \"swap\");\n        }\n        TRACE(9, i, -1, min_idx, \"pass\");\n    }\n}",
"insertion":"void sort(int a[], int n) {\n    for (int i = 1; i < n; i++) {\n        int key = a[i], j = i-1;\n        while (j >= 0 && a[j] > key) {\n            a[j+1] = a[j];\n            TRACE(6, i, j, key, \"shift\");\n            j--;\n        }\n        a[j+1] = key;\n        TRACE(8, i, j+1, key, \"insert\");\n    }\n}",
"quick":"int partition(int a[], int low, int high) {\n    int pivot = a[high], i = low-1;\n    for (int j = low; j < high; j++) {\n        TRACE(3, i, j, pivot, \"compare\");\n        if (a[j] < pivot) {\n            i++; swap(a[i], a[j]);\n            TRACE(6, i, j, pivot, \"partition-swap\");\n        }\n    }\n    swap(a[i+1], a[high]);\n    TRACE(9, i+1, high, pivot, \"pivot\");\n}",
"merge":"void merge(int a[], int l, int m, int r) {\n    copy halves into L[] and R[];\n    int i=0, j=0, k=l;\n    while (i<n1 && j<n2) {\n        // compare the front elements\n        if (L[i] <= R[j]) a[k++] = L[i++];\n        else a[k++] = R[j++];\n        TRACE(8, i, j, k-1, \"write\");\n    }\n    while (i<n1) { a[k++] = L[i++]; TRACE(10,...); }\n    while (j<n2) { a[k++] = R[j++]; TRACE(11,...); }\n}\nvoid divide(int a[], int l, int r) {\n    if (l < r) {\n        int m = (l+r)/2; TRACE(14,l,r,m,\"divide\");\n        divide(a,l,m); divide(a,m+1,r); merge(a,l,m,r);\n    }\n}",
"heap":"void heapify(int a[], int n, int i) {\n    int largest=i, left=2*i+1, right=2*i+2;\n    if (left<n && a[left]>a[largest]) largest=left;\n    TRACE(4, i, largest, n, \"compare\");\n    if (largest != i) {\n        swap(a[i], a[largest]);\n        TRACE(7, i, largest, -1, \"swap\");\n    }\n}\nvoid sort(int a[], int n) {\n    build_max_heap(a,n);\n    swap(a[0],a[i]); TRACE(11,0,i,-1,\"extract\");\n}",
"counting":"void sort(int a[], int n) {\n    int count[100]={0}, output[256];\n    for (int i=0; i<n; i++) { count[a[i]]++; TRACE(2,i,-1,a[i],\"count\"); }\n    prefix_sum(count);\n    for (int i=n-1; i>=0; i--) {\n        output[--count[a[i]]] = a[i];\n        TRACE(5,i,-1,a[i],\"place\");\n    }\n    for (int i=0; i<n; i++) { a[i]=output[i]; TRACE(6,i,-1,a[i],\"write\"); }\n}",
"radix":"void sort(int a[], int n) {\n    find_maximum(a,n);\n    for (int exp=1; max/exp>0; exp*=10) {\n        count_digit_frequencies(a,count,exp); TRACE(3,i,-1,exp,\"digit-count\");\n        prefix_sum(count);\n        for (int i=n-1; i>=0; i--) {\n            output[--count[digit]] = a[i];\n            TRACE(7,i,digit,exp,\"digit-place\");\n        }\n        copy_output_back(a,output); TRACE(8,i,-1,exp,\"digit-write\");\n    }\n}"
}
@app.get('/')
def home(): return render_template('index.html',algorithms=ALG)
@app.get('/api/algorithm/<key>')
def info(key):
    if key not in ALG:return jsonify(error='Unknown algorithm'),404
    a=ALG[key];return jsonify(name=a[0],complexity=a[1],space=a[2],code=DISPLAY[key])
@app.post('/api/run')
def run():
    d=request.get_json(force=True);key=d.get('algorithm');arr=d.get('array')
    if key not in ALG:return jsonify(error='Unknown algorithm'),400
    if not isinstance(arr,list) or not 2<=len(arr)<=40:return jsonify(error='Use 2–40 values.'),400
    try:arr=[int(x) for x in arr]
    except:return jsonify(error='Only integers are allowed.'),400
    if any(x<0 or x>99 for x in arr):return jsonify(error='Use values from 0 to 99.'),400
    gcc=shutil.which('gcc')
    if not gcc:return jsonify(error='GCC not found. Install GCC and add it to PATH.'),500
    with tempfile.TemporaryDirectory() as td:
        c=os.path.join(td,'sort.c');exe=os.path.join(td,'sort.exe')
        open(c,'w').write(source(key,arr))
        cp=subprocess.run([gcc,c,'-O0','-o',exe],capture_output=True,text=True,timeout=10)
        if cp.returncode:return jsonify(error=cp.stderr),500
        p=subprocess.run([exe],capture_output=True,text=True,timeout=3)
        events=[]
        for line in p.stdout.splitlines():
            try:events.append(json.loads(line))
            except:pass
    a=ALG[key]
    return jsonify(events=events,name=a[0],complexity=a[1],space=a[2],source=DISPLAY[key])
if __name__=='__main__':app.run(host='127.0.0.1',port=5000)
