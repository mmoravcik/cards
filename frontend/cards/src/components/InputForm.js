import React from 'react';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import MenuItem from '@material-ui/core/MenuItem';
import Select from '@material-ui/core/Select';


class InputForm extends React.Component {
  constructor() {
    super();
    this.state = {
      deckActions: [],
      deckAction: 'shuffle',
    };
  }

  handleChange = event => {
    this.setState({ [event.target.name]: event.target.value });
  };


  render() {
    return (
      <React.Fragment>
        <Grid container spacing={24}>
          <Grid item xs={12} sm={12}>
            <TextField
              required
              type="number"
              id="numberOfCards"
              name="numberOfCards"
              label="Number of non-joker cards"
              defaultValue="52"
            />
          </Grid>
          <Grid item xs={12} sm={12}>
            <TextField
              required
              type="number"
              id="numberOfJokers"
              name="numberOfJokers"
              label="Number of jokers"
              defaultValue="0"
            />
          </Grid>
          <Grid item xs={12} sm={12}>
            <Select
              required
              value={this.state.deckAction}
              onChange={this.handleChange}
              inputProps={{
                name: 'deckAction',
                id: 'deck-action',
              }}
            >
              <MenuItem value="shuffle">Shuttle the deck</MenuItem>
              <MenuItem value="pick-random">Pick a random card</MenuItem>
              <MenuItem value="pick-specific">Pick a card</MenuItem>
            </Select>
          </Grid>
        </Grid>
      </React.Fragment>
    );
  }
}

export default InputForm;