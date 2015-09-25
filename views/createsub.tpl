<h2>Success!</h2>
OK: created {{res}}!<p>
%x = res.split("/")
%l = ""
%for i in range(1,len(x)-1):
	%l += "|%s" % x[i]
	<a href="{{l}}">/{{x[i]}}</a>
%end
<script type="text/javascript">
  setTimeout(function(){
    location = '{{last_url}}';
  }, 1000);
</script>
