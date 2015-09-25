<html>
<h2>
%x = res[0].split("/")
%l = ""
%for i in range(1,len(x)-1):
        %l += "|%s" % x[i]
        <a href="{{l}}">/{{x[i]}}</a>
%end
/{{x[len(x)-1]}} </h2>
<a href="/create/{{res[0].replace("/","|")}}" class="btn btn-default">create new leaf node</a><hr>
<table class="table table-striped">
%for i in sorted(res[1].keys()):
	%root = res[0].replace("/","|")
	<tr>
	<td width="140px">
	%if res[1][i]:
		%element_id = i.replace('.', '-')
		<a class="btn btn-default btn-xs" role="button" data-toggle="collapse" href="#collapse{{element_id}}" aria-expanded="false" aria-controls="collapse{{element_id}}">show content</a>
		<a class="btn btn-primary btn-xs" href="/edit/{{root}}|{{i}}">edit</a>
	%else:
		%element_id = ''
	%end
		</td>
		<td>
			<span><a href="/{{root}}|{{i}}">{{i}}</a></span>
			<div id="collapse{{element_id}}" class="panel-collapse collapse" role="tabpanel">
	      <div class="panel-body">
					<pre>{{res[1][i]}}</pre><hr width=50% align=left>
				</div>
			</div>
		</td>
		<td style="text-align:right">
	%if res[2] == 'T':
		<a class="btn btn-danger btn-xs" href="/delete/{{root}}|{{i}}" onclick="return confirm('Are you sure you want to delete {{i}}?')">&times;</a>
	%end
		</td>
	</tr>
%end
</table>
