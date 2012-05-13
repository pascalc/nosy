require 'sinatra'

get '/' do
    erb :index
end

post '/classify/text' do
  "ok"
end

__END__

@@index
<!DOCTYPE html>
<html>
<head>
  <meta name="charset" content="utf-8">
  <title>Classify text</title>
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

    #text-input {
      width: 100%;
      height: 50px;
    }
  </style>
</head>

<body>
<div id="main-column">
  <h1>Classify text</h1>
  
  <form id="text-form" method="post" action="/classify/text">
    <label for="text-input">Enter text to classify</label>
    <br/>
    <textarea id="text-input"></textarea>
    <br/>
    <input id="start-button" type="submit" value="Classify" />
  </form>

  <div id="result-container">
  </div> 

  <script type="text/javascript" charset="utf-8">
    $(document).ready(function(){
      // Start stream via AJAX
      $("#start-button").click(function(e) {
        e.preventDefault();

        var $form = $('form#text-form');
        var url = $form.attr('action');
        var text = $('#text-input').text();
        
        console.log('Data sent to server: ', text);
        $.post(url, {text: text}, function(result) {
          console.log(result);
          $('#result-container').html(
            '<p>The text was classified as <strong>'+result+'</strong></p>'
          );
        });
      });
    });
  </script>
</body>
</html>