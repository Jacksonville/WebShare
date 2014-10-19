<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Ad Hoc File Share</title>
    <link rel="stylesheet" href="/static/css/foundation.css" />
    <script src="/static/js/vendor/modernizr.js"></script>
</head>
<body>
    <div class="row">
      <div class="large-12 columns">
        <h1>AD Hoc File Share</h1>
      </div>
    </div>
    <div class="row">
        <a href="/?dir={{curr_dir[:-1].replace(curr_dir[:-1].split('/')[-1],'')[:-1]}}">Up</a>
    </div>
    %for dir in dirlist:
    <div class="row">
        <a href="/?dir={{curr_dir}}{{dir}}">{{dir}}</a>
    </div>
    %end
    %for file in filelist:
    <div class="row">
        <a href="/dl?filename={{curr_dir}}{{file}}">{{file}}</a>
    </div>
    %end
    <script src="/static/js/vendor/jquery.js"></script>
    <script src="/static/js/foundation.min.js"></script>
    <script>
      $(function(){
          $(document).foundation();
      });
    </script>
</body>
</html>
