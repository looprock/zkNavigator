<h2>Success!</h2>
OK: updated {{res[1]}}!<p>
%x = res[0].split("|")
%l = ""
%last_url = ""
%for i in range(1,len(x)-1):
	%l += "|%s" % x[i]
  %last_url = l
	<a href="{{l}}">/{{x[i]}}</a>
%end
<script type="text/javascript">
  setTimeout(function(){
    location = '{{last_url}}';
  }, 1000);
</script>
