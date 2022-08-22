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



class AddQuoteForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      is_loaded: false,
      form_author: null,
      show_author_input: false,
      form_quote: null,
      all_authors: []
    };
  }



  async load_authors() {
    var authors;
    const response = await fetch("/api/who-said-that/authors");
    authors = await response.json();
    this.setState({all_authors: authors})
  }

  componentDidMount() {
    this.load_authors();
  }


  upload_quote = (e) => {
    e.preventDefault();
    var data = {"quote": {"text": this.state.form_quote, "author": this.state.form_author}};
    console.log(data);
    fetch("/api/who-said-that/upload-quote", {"method": "POST", "body": JSON.stringify(data)})
      .then(res => {
        console.log("Request complete! response:", res);
      })
  }


  handle_change_select = async (e) => {
    var name = e.target.name;
    var value = e.target.value;
    if (!value)
      await this.setState({show_author_input: true})
    else
      await this.setState({show_author_input: false})
    await this.setState({[name]: value});
    console.log(this.state);
  }


  handle_change_input = async (e) => {
    var name = e.target.name;
    var value = e.target.value;
    await this.setState({[name]: value});
    console.log(this.state);
  }

  render() {
    const { error, is_loaded, show_author_input, all_authors} = this.state;

    return (      
      <form id="quote_form" onSubmit={this.upload_quote}>
        <label>Quote<input type="text" name="form_quote" onChange={this.handle_change_select}/></label>
        <label>Author
          <select name="form_author" onChange={this.handle_change_select}>
            <option value=''>Add new</option>
            { all_authors.map((author, index) => {
              return (
                  <option value={author}>{author.name}</option>
                )
            })}
          </select>
          {show_author_input ? <input type="text" name="form_author" onClick={this.handle_change_input}/> : null}
        </label>
        <button type="submit">Submit</button>
      </form> 
      )
  }

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
      answer: null,
      show_upload_quote_form: false,
      form_author: null,
      form_quote: null,
      all_authors: []
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

  show_upload_quote_form = (e) => {
      this.setState({show_upload_quote_form: true});
  }
 
  render() {
    const { error, is_loaded, quote, authors, guess, answer, answer_index, show_upload_quote_form, all_authors} = this.state;
    var win, option_status, disabled, span_text, anchor_text;

    if (guess != null) {
      if (guess == answer_index) {
        win = true;
        option_status = "win";
        span_text = "Yes! " + authors[guess].name + " did say that, nice catch!";
        anchor_text = "One more time?";
      }
      else {
        win = false;
        option_status = "lose";
        span_text = "Unfortunately, no. This quote actually belongs to " + authors[guess].name + ".";
        anchor_text = "Try again?";
      }

      disabled = true;
    }

    if (error) {
      return ({error})
    }
    else if (!is_loaded) {
      return ("Loading...")
    } 
    else {
      return (
          <div>
            <p className="quote">{ quote }</p>
            <div className="options">
              { authors.map((author, index) => {
                return (
                 <div className={(guess == index) ? "option " + option_status : "option"} key={index.toString()}>
                   <button className="author" onClick={this.poll_results} disabled={disabled}>{ author.name }</button>
                 </div>
                )
              }) }
              {<p>{span_text}</p>}
              {<a href="#" onClick={this.update_poll}>{anchor_text}</a>}
            </div>
            {/*<p>Wanna see your quote here? <a href="#" onClick={this.show_upload_quote_form}>Click here</a></p>
            {show_upload_quote_form ? <AddQuoteForm/> : null}*/}
          </div>
        )
    }
  }
}

const domContainer = document.querySelector('#who_said_that');
const root = ReactDOM.createRoot(domContainer);
root.render(e(WhoSaidThatPoll));