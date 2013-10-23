<h2>{{res.replace("|","/")}}</h2>
<form name="myform" action="/createsub" method="POST">
Node 
<input name="node" type="text" /><br>
Content:<br>
<textarea cols="80" rows="20" name="content">
</textarea>
<input type="hidden" name="path" value="{{res}}">
<p><input type="submit" value="Create">
</form>
