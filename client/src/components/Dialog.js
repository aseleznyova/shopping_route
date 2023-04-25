import * as React from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import Typography from '@mui/material/Typography';
import DialogTitle from '@mui/material/DialogTitle';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { useState, useEffect} from "react";

const theme = createTheme({
  palette: {
    green: {
      main: '#4CAF50',
      contrastText: '#fff'
    },
  },
  });

export default function AlertDialog({open, setOpen, title, text}) {
  const [info, setInfo] = useState([]);
  useEffect(()=>{
    if(!info.length && text !== ''){
      split_text(text);
    }
},[])
  const handleClose = () => {
    setOpen(false);
  };
  function split_text(text_to_split){
    let ans = [];
    let text_array = text_to_split.split('\n');
    for(let i = 0; i < text_array.length; i++){
      ans.push(<Typography gutterBottom>
        {text_array[i]}
      </Typography>);
    }
    setInfo(ans)
  }

  return (
    <div>
    <ThemeProvider theme={theme}>
      <Dialog
        open={open}
        onClose={handleClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">
          {title}
        </DialogTitle>
        <DialogContent>
            {info}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="green" variant="contained">
            Закрыть
          </Button>
        </DialogActions>
      </Dialog>
      </ThemeProvider>
    </div>
  );
}
