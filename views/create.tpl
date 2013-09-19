<h2>{{res[0].replace("|","/")}}</h2>
<form name="myform" action="{{res[1]}}/createsub" method="POST">
Node 
<input name="node" type="text" /><br>
Content:<br>
<textarea cols="80" rows="20" name="content">
</textarea>
<input type="hidden" name="path" value="{{res[0]}}">
<p><input type="submit" value="Create">
</form>
