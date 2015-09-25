<link rel="stylesheet" href="https://cdn.jsdelivr.net/g/codemirror@4.5.0(addon/display/fullscreen.min.css+addon/fold/foldgutter.min.css+addon/fold/foldgutter.css+addon/hint/show-hint.min.css+addon/hint/show-hint.css+codemirror.css)">
<style>
  .CodeMirror {
    border: 1px solid #eee;
    height: auto;
  }
</style>

<script src="https://cdn.jsdelivr.net/g/codemirror@4.5.0(codemirror.min.js+addon/display/fullscreen.js+addon/fold/brace-fold.js+addon/fold/foldcode.js+addon/fold/foldgutter.js+addon/fold/indent-fold.js+addon/fold/xml-fold.js+addon/hint/anyword-hint.js+addon/hint/show-hint.js+addon/hint/xml-hint.js+mode/htmlmixed/htmlmixed.js+mode/javascript/javascript.js+mode/xml/xml.js+mode/yaml/yaml.js+mode/properties/properties.js)"></script>

<script type="text/javascript">
  var types = {
  "ini": "properties",
  "html": "htmlmixed",
  "htm": "htmlmixed",
  "js": "javascript",
  "_js": "javascript",
  "json": "javascript",
  "xml": "xml",
  "wxs": "xml",
  "wxl": "xml",
  "wsdl": "xml",
  "xslt": "xml",
  "xsl": "xml",
  "xul": "xml",
  "xbl": "xml",
  "config": "xml",
  "xaml": "xml",
  "sql": "sql",
  "md": "markdown",
  "yaml": "yaml",
  "yml": "yaml"
  };

  var filename = "{{res[0]}}";
  var ext = filename.split('.').pop();

  var editor = CodeMirror.fromTextArea(document.getElementsByTagName('textarea')[0], {
    lineNumbers: true,
    matchBrackets: true,
    mode: types[ext] ? types[ext] : undefined,
    viewportMargin: Infinity
  });
</script>
