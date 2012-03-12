require 'sinatra'

get '/' do
    erb :index
end

__END__

@@index
<!DOCTYPE html>
<html>
<head>
  <meta name="charset" content="utf-8">
  <title>Twitter Stream</title>
  <script src="http://nosy.pspace.se:8080/application.js" type="text/javascript" charset="utf-8"></script>
  <script src="http://code.jquery.com/jquery-1.7.1.min.js"></script>

  
  <style type="text/css" media="screen">
    body {
        font-size: 18px;
        font-family: 'Georgia';
        width: 500px;
        margin-right: auto;
        margin-left: auto;
    }

    h1 {
      margin: 0.5rem 0 1.5rem 0;
      font-family: 'Helvetica Neue';
      font-weight: bold;
      text-align: center;
      font-size: 50px;
    }
    
    #stream {
      line-height: 1.8rem;
      max-height: 800px;
      overflow-y: scroll;
    }
  </style>
</head>
<body>

  <h1>Twitter Stream</h1>
  
  <form method="post" action="http://nosy.pspace.se:7777/classify/stream"> 
    <input id="start-button" type="submit" value="Start" /> 
  </form>

  <section id="stream"></section>
  
  <script type="text/javascript" charset="utf-8">
    $(document).ready(function(){
      // Start stream via AJAX
      $("#start-button").click(function(e) {
        e.preventDefault();
        $.post("http://nosy.pspace.se:7777/classify/stream", function(data) {
          console.log(data);
        });
      });

      // Juggernaut
      var show = function(data){
        var authorLink = "<a href=http://twitter.com/" + data.author + "><strong>@" + data.author + ":</strong></a>";
        var geoInfo = " <em>location: (" + data.location + ")</em>";
        var line = "<p>" + authorLink + data.text + geoInfo + "</p>";
        $(line).hide().prependTo("#stream").fadeIn("slow");
      };

      var jug = new Juggernaut({
        secure: ('https:' == document.location.protocol),
        host: document.location.hostname,
        port: 8080
      });

      jug.subscribe("nosy", function(data){
        show(data);
        console.log("Got: " + data);
      });
    });
  </script>
</body>
</html>