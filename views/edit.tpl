<h2>{{res[0]}}</h2>
<form name="myform" action="/editsub" method="POST">
<textarea class="form-control" cols="80" rows="20" name="content">
%x = res[1]
{{!x}}
</textarea>
%c = res[0].replace("/","|")
<input type="hidden" name="node" value="{{c}}">
<br><input class="btn btn-primary" type="submit" value="Save">
<input class="btn btn-default" type="button" value="Back" onclick="history.go(-1)">
</form>

%include('editor.tpl')
