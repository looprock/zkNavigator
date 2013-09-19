<h2>{{res[0]}}</h2>
<form name="myform" action="{{res[2]}}/editsub" method="POST">
<textarea cols="80" rows="20" name="content">
%x = res[1]
{{!x}}
</textarea>
%c = res[0].replace("/","|")
<input type="hidden" name="node" value="{{c}}">
<p><input type="submit" value="Edit">
</form>
