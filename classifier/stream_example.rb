require 'sinatra'

get '/' do
    erb :index
end

post '/classify/stream' do
  current_dir = File.dirname(__FILE__)
  p = fork { system("python #{current_dir}/tweet_classifier.py -processes 1 -tweets 1000 YAP_nosy yetanotherproject") }
  Process.detach(p)
  "ok"
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
<div id="main-column">
  <h1>Twitter Stream</h1>
  
  <form id="stream-form" method="post" action="/classify/stream">
    
    <div id="language-selection">
      <label for="lang">Select language</label>
      <select name="lang" id="lang">
        <option value="en" selected="selected">English</option>
        <option value="se">Swedish</option>
      </select>
      <br/>
      <label for="lang-threshold">Enter threshold (0,1)</label>
      <input type="text" value="0.5" id="lang-threshold" />
      <br/>
      <button id="lang" onclick="addTags(this)">Add language</button>
    </div>
    
    <br/>

    <div id="tags-selection">
      <label for="tags">Select tag</label>
      <select name="tags" id="tags">
        <option value="tag1">Tag1</option>
        <option value="tag2">Tag2</option>
      </select>
      <br/>
      <label for="tags-threshold">Enter threshold (0,1)</label>
      <input type="text" value="0.5" id="tags-threshold" />
      <br/>
      <button id="tags" onclick="addTags(this)">Add tag</button>
    </div>
    <br/>

    <input id="start-button" type="submit" value="Start" />
  </form>

  <h2>Language</h2>
  <div id="lang-list"><ul class="tags-list"></ul></div>
  <h2>Tags</h2>
  <div id="tags-list"><ul class="tags-list"></ul></div>
  <section id="stream"></section>
  
   

  <script type="text/javascript" charset="utf-8">
    function addTags(elem) {
      var type = elem.id;
      var $selected = $('select[id="'+type+'"]').find('option').filter(':selected');
      var threshold = $('input[id="'+type+'-threshold"]').val();
      var lang = $selected.val();
      var disp = $selected.text() + ' : ' + threshold;
      var id = lang+':'+threshold;
      append(type+'-list', disp, id);
    }

    function append(type, text, id) {
      css = {
        'margin-left':'15px',
        'cursor': 'pointer'
      };
      $('#'+type).find('ul').append(
          $('<li>').attr({'id': id}).text(text).append(
            $('<span>').attr({'class':'remove'}).css(css).text('X')
          )
      );
    }

    $(document).ready(function(){
      // Start stream via AJAX
      $("#start-button").click(function(e) {
        e.preventDefault();

        var $form = $('form#stream-form');
        var url = $form.attr('action');

        var tags = {};
        $('ul.tags-list li').each(function(i, elem) {
           var tmp = $(elem).attr('id').split(':');
           tags[''+tmp[0]] = tmp[1];
        });
        console.log('Data sent to server: ', tags);
        $.post(url, {tags: tags}, function(data) {
          console.log(data);
        });
      });

      $('span.remove').live('click', function() {
        $(this).parent('li').remove();
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