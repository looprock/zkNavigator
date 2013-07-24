<html>
<h2>
%x = res[0].split("/")
%l = ""
%for i in range(1,len(x)-1):
        %l += "|%s" % x[i]
        <a href="{{l}}">/{{x[i]}}</a>
%end
/{{x[len(x)-1]}} </h2> 
<a href="/create/{{res[0].replace("/","|")}}">create new leaf node</a><hr><p>
%for i in res[1].keys():
	%root = res[0].replace("/","|")
	<a href="/{{root}}|{{i}}">{{i}}</a>
	%if res[2] == 'T':
		 - [<a href="/delete/{{root}}|{{i}}">delete</a>]
	%end
	<br>
	%if res[1][i]:
		<hr width=50% align=left><b>CONTENT:</b> (<a href="/edit/{{root}}|{{i}}">edit</a>)<br>
		<pre>{{res[1][i]}}</pre><hr width=50% align=left>
	%end
	<p>
%end
