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

class WhoSaidThatPoll extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      quote: null,
      authors: null,
    };
  }

  componentDidMount() {
    fetch("/api/who-said-that/random")
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            quote: result["text"],
            authors: result["authors"]
          });
        },
        // Note: it's important to handle errors here
        // instead of a catch() block so that we don't swallow
        // exceptions from actual bugs in components.
        (error) => {
          this.setState({
            isLoaded: true,
            error
          });
        }
      )
  }

  poll_results = (e) => {
    const authors = this.state.authors;
    var author = authors.find(a => a.name === e.target.outerText);
    if (author.real) {
      console.log("You win!");
      e.target.classList.add("win");
    }
    else {
      console.log("You lose!")
      e.target.classList.add("lose");
    }
    e.target.disabled = true;
    console.log(e.target);
  }

  render() {
    const { error, isLoaded, quote, authors } = this.state;
    if (error) {
      return ({error})
    }
    else if (!isLoaded) {
      return ("Loading...")
    } 
    else {
      var shuffled_authors = shuffle(authors);
      console.log(shuffled_authors);

      return (
          <div>
            <p class="quote">{ quote }</p>
            <div class="options">
            { shuffled_authors.map((author, index) => {
              return (
                <button class="author" key={index.toString()} onClick={this.poll_results}>{ author.name } </button>
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