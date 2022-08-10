'use strict';

function shuffle(array) {
  let currentIndex = array.length,  randomIndex;

  // While there remain elements to shuffle.
  while (currentIndex != 0) {

    // Pick a remaining element.
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex--;

    // And swap it with the current element.
    [array[currentIndex], array[randomIndex]] = [
      array[randomIndex], array[currentIndex]];
  }

  return array;
}


const e = React.createElement;

function PollOption(props) {
  console.log(props);
  let span_text, anchor_text, win, option_status, disabled;

  if (props.guess != null) {
    if (props.guess == props.answer_index)
      win = true
    else
      win = false

    if (props.index == props.guess) {
      if (win) {
        option_status = "option win";
        span_text = "Yes! " + props.author.name + " did say that, nice catch!";
        anchor_text = "One more time?";
      }
      else {
        option_status = "option lose";
        span_text = "Unfortunately, no. This quote actually belongs to " + props.answer.name + ".";
        anchor_text = "Try again?";
      }    
    }
    
    disabled = true;
  }
  else {
    option_status = "option";
    disabled = false;
  }

  return (
   <div class={option_status} key={props.index.toString()}>
     <button class="author" onClick={props.poll_results} disabled={disabled}>{ props.author.name }</button>
     {props.index == props.guess ? <span>{span_text} <a href="#" onClick={props.update_poll}>{anchor_text}</a></span> : null}
   </div>
  )  
}

class WhoSaidThatPoll extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      is_loaded: false,
      quote: null,
      authors: null,
      guess: null,
      answer: null
    };
  }

  update_poll = () => {
    this.setState({
      error: null,
      is_loaded: false,
      quote: null,
      authors: null,
      guess: null,
      answer: null
    });
    fetch("/api/who-said-that/random")
      .then(res => res.json())
      .then(
        (result) => {
          let authors = shuffle(result["authors"]);
          let answer = authors.find(a => a.real === true);
          let answer_index = authors.indexOf(answer);
          this.setState({
            is_loaded: true,
            quote: result["text"],
            authors: authors,
            answer: answer,
            answer_index: answer_index
          });
        },
        (error) => {
          this.setState({
            is_loaded: true,
            error: error
          });
        }
      )
  }

  componentDidMount() {
    this.update_poll();
  }

  poll_results = (e) => {
    const authors = this.state.authors;
    this.setState({"guess": authors.indexOf(authors.find(a => a.name === e.target.outerText))});
  }

  render() {
    const { error, is_loaded, quote, authors, guess, answer, answer_index } = this.state;
    if (error) {
      return ({error})
    }
    else if (!is_loaded) {
      return ("Loading...")
    } 
    else {
      return (
          <div>
            <span class="quote">{ quote }</span>
            <div class="options">
            { authors.map((author, index) => {
              return (
                <PollOption
                  poll_results={this.poll_results}
                  update_poll={this.update_poll}
                  author={author}
                  index={index}
                  guess={guess}
                  answer={answer}
                  answer_index={answer_index}
                />
              )
            }) }
            </div>
          </div>
        )
    }
  }
}

const domContainer = document.querySelector('#who_said_that');
const root = ReactDOM.createRoot(domContainer);
root.render(e(WhoSaidThatPoll));