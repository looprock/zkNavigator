<h2>{{res.replace("|","/")}}</h2>
<form name="myform" action="/createsub" method="POST">
Node
<input class="form-control" name="node" type="text" /><br>
Content:<br>
<textarea class="form-control" cols="80" rows="20" name="content">
</textarea>
<input type="hidden" name="path" value="{{res}}">
<br><input class="btn btn-primary" type="submit" value="Create">
</form>

%include('editor.tpl')
