<h2>Success!</h2>
OK: updated {{res[1]}}!<p>
%x = res[0].split("|")
%l = ""
%for i in range(1,len(x)-1):
	%l += "|%s" % x[i]
	<a href="{{res[2]}}/{{l}}">/{{x[i]}}</a> 
%end
