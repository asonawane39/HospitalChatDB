import { faPaperPlane, faRotateRight, faUserNurse, faRightFromBracket} from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import 'bootstrap/dist/css/bootstrap.min.css';
import React, { useEffect, useRef, useState } from 'react';
import './Chatbot.css';
 

function Chatbot({onLogout}) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [showExampleQuestions, setShowExampleQuestions] = useState(false);  
  const [isNewChat, setIsNewChat] = useState(true);
  const [isExitDialogOpen, setIsExitDialogOpen] = useState(false);
  const [isLogoutDialogOpen, setIsLogoutDialogOpen] = useState(false);
  const [isChatVisible, setIsChatVisible] = useState(true);
  const [isStartNewChatDialogOpen, setIsStartNewChatDialogOpen] = useState(false);
  const [showTodayText, setShowTodayText] = useState(false);
  const chatWindowRef = useRef(null);

  const api = "http://127.0.0.1:8000";
  const formatMultipleReponseIntoTable = (data) => {
    let colnames = Object.keys(data);
    let numRows = data[colnames[0]].length;
  
    let tableString = '<table border="1">\n';
  
    // Add header row
    tableString += '  <tr>';
    for (let col of colnames) {
      tableString += `<th>${col}</th>`;
    }
    tableString += '</tr>\n';
  
    // Add data rows
    for (let i = 0; i < numRows; i++) {
      tableString += '  <tr>';
      for (let col of colnames) {
        tableString += `<td>${data[col][i]}</td>`;
      }
      tableString += '</tr>\n';
    }
  
    tableString += '</table>';
    return tableString;
  };
  
    const formatTimestamp = (date) => {
      let hours = date.getHours();
      const minutes = date.getMinutes().toString().padStart(2, '0');
      const period = hours >= 12 ? 'PM' : 'AM';
    
      hours = hours % 12;
      hours = hours ? hours : 12;
      
      return `${hours}:${minutes} ${period}`;
    };

    const addMessage = (text, sender, type="text", isTyping = false) => {
      const newMessage = {
        sender,
        text,
        type,
        isTyping,
        timestamp: formatTimestamp(new Date()),
      };
      setMessages((prevMessages) => [...prevMessages, newMessage]);
    };

    const fetchChatResponse = (userInput) => {
        // addMessage('', 'bot', true);

        // setTimeout(() => {
        //     setMessages((prevMessages) => prevMessages.filter((msg) => !msg.isTyping));
        // userInput= userInput.toLowerCase();

        // let botResponse = "I'm sorry, I do not understand.";
        // if (userInput.includes("name for medicine id 0025"))
        // {
        //   botResponse = "{ 'message': 'Done!!', 'status': 'success', 'data': {'medicine_name': 'Levofloxacin 500mg'}, 'response_length': 'single', 'dataheaders': ['medicine_name']} \n \n Done!! \n medicine_name: Levofloxacin 500mg ";
        // }
        // else if (userInput.includes("ighest prescribed medicine"))
        // {
        //   botResponse = "{ 'message': 'Done!!', 'status': 'success', 'data': [{'_id': '0025', 'count': 1713}], 'response_length': 'multiple', 'dataheaders': ['medicine_id', 'count'}]\n  \n Done!!\n medicine_id: 0025, count: 1713}";
        // }
        // else if (userInput.includes("many prescriptions are there"))
        // {
        //   botResponse = "{'message': 'Done!!', 'status': 'success', 'data': 6052, 'response_length': 'single', 'dataheaders': ['total perscriptions']} \n \n Done!!\ntotal perscriptions: 6052 ";
        // }

    
      
        // addMessage(botResponse, 'bot');
        // }, 2000);

        
        fetch(`${api}/server/get_response`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ query: userInput }),
        })
        .then((response) => response.json())
        .then((data) => {
          if (data.response.response_length == 'multiple')
            addMessage(formatMultipleReponseIntoTable(data.response.data), 'bot', "table");
          else {
            
            let botResponse = JSON.stringify(data.response.data);
            addMessage(`there are ${botResponse} records...`, 'bot');
          }

        })
        .catch((error) => {
          console.error("API error:", error);
          addMessage("Could not connect to server.", 'bot');
        });
        return;
        
    };

    const handleSendMessage = async (message = input) => {
      const trimmedInput = message.trim();
      if (!trimmedInput) return;
      
      addMessage(trimmedInput, 'user');
    
      fetchChatResponse(trimmedInput);
    
      setInput('');
      setShowExampleQuestions(false);
    };

    const handleKeyPress = (e) => {
      if (e.key === 'Enter' && !messages.some((msg) => msg.isTyping)) {
        handleSendMessage();
      }
    };

    const handleExampleQuestionClick = (question) => {
      handleSendMessage(question);
    
      setShowExampleQuestions(false);
    };

    // useEffect(() => {
    //   if (chatWindowRef.current) {
    //     if (showExampleQuestions) {
    //       setTimeout(() => {
    //         chatWindowRef.current.scrollTo({
    //           top: chatWindowRef.current.scrollHeight,
    //           behavior: 'smooth',
    //         });
    //       }, 100);
    //     } else {
    //       chatWindowRef.current.scrollTo({
    //         top: chatWindowRef.current.scrollHeight,
    //         behavior: 'smooth',
    //       });
    //     }
    //   }
    // }, [messages, showExampleQuestions]);
    useEffect(() => {
      if (chatWindowRef.current) {
        if (showExampleQuestions) {
          setTimeout(() => {
            chatWindowRef.current.scrollTo({
              top: chatWindowRef.current.scrollHeight,
              behavior: 'smooth',
            });
          }, 100);
        } else {
          chatWindowRef.current.scrollTo({
            top: chatWindowRef.current.scrollHeight,
            behavior: 'smooth',
          });
        }
      }
    });
   
    useEffect(() => {
      const timeout0 = setTimeout(() => {
        setMessages((prevMessages) => [
          ...prevMessages,
          { sender: 'bot', text: '', isTyping: true, timestamp: formatTimestamp(new Date()) },
        ]);
      }, 0);
    
      const timeout1 = setTimeout(() => {
        setMessages((prevMessages) => {
          const newMessages = prevMessages.filter(msg => !msg.isTyping);
          newMessages.push({
            sender: 'bot',
            text: "Hello! Welcome to the database chatbot for our hospital, where you can easily search for anything in our database!",
            timestamp: formatTimestamp(new Date()),
          });
          return newMessages;
        });
      }, 2000);
    
      const timeout2 = setTimeout(() => {
        setMessages((prevMessages) => [
          ...prevMessages,
          { sender: 'bot', text: '', isTyping: true, timestamp: formatTimestamp(new Date()) },
        ]);
      }, 2200);
    
      const timeout3 = setTimeout(() => {
        setMessages((prevMessages) => {
          const newMessages = prevMessages.filter(msg => !msg.isTyping);
          newMessages.push({
            sender: 'bot',
            text: 'What can I help you find today?',
            timestamp: formatTimestamp(new Date()),
            icon: {faUserNurse},
          });
          return newMessages;
        });
      }, 5000);
    
      const timeout4 = setTimeout(() => {
        setShowExampleQuestions(true);
      }, 5200);
   
      return () => {
        clearTimeout(timeout0);
        clearTimeout(timeout1);
        clearTimeout(timeout2);
        clearTimeout(timeout3);
        clearTimeout(timeout4);
      };
    }, []);
   
    const exampleQuestions = [
      "What is the medicine name for medicine id 0025?",
      "What is the highest prescribed medicine?",
      "How many prescriptions are there in total?"
    ];
   
    const openExitDialog = () => {
      if (!isStartNewChatDialogOpen) {
        setIsExitDialogOpen(true);
      } else {
        setIsChatVisible(false);
      }
    };
   
    const closeExitDialog = () => {
      setIsExitDialogOpen(false);
    };

    const openLogoutDialog = () => {
      if (!isStartNewChatDialogOpen) {
        setIsLogoutDialogOpen(true);
      } else {
        setIsChatVisible(false);
      }
    };
   
    const closeLogoutDialog = () => {
      setIsLogoutDialogOpen(false);
    };
   
   
    const endChat = () => {
      setIsExitDialogOpen(false);
      setMessages([]);
      setShowTodayText(false);
      setIsNewChat(true);
      setIsChatVisible(true);
      setShowExampleQuestions(false);

    
      setMessages([
        { sender: 'bot', text: '', isTyping: true, timestamp: formatTimestamp(new Date()) },
      ]);
    
      setTimeout(() => {
        setMessages((prevMessages) => {
          const newMessages = prevMessages.filter(msg => !msg.isTyping);
          newMessages.push({
            sender: 'bot',
            text: "Hello! Welcome to the database chatbot for our hospital, where you can easily search for anything in our database!",
            timestamp: formatTimestamp(new Date()),
          });
          return newMessages;
        });
      }, 2000);
    
      setTimeout(() => {
        setMessages((prevMessages) => [
          ...prevMessages,
          { sender: 'bot', text: '', isTyping: true, timestamp: formatTimestamp(new Date()) },
        ]);
      }, 2200);
    
      setTimeout(() => {
        setMessages((prevMessages) => {
          const newMessages = prevMessages.filter(msg => !msg.isTyping);
          newMessages.push({
            sender: 'bot',
            text: 'What can I help you find today?',
            timestamp: formatTimestamp(new Date()),
            
          });
          return newMessages;
        });
      }, 5000);
    
      setTimeout(() => {
        setShowExampleQuestions(true);
      }, 5200);
    };
    

    return (
      <>
        <div className={`chatbot-container ${!isChatVisible ? 'd-none' : ''}`}>
          {isExitDialogOpen && <div className="overlay"></div>}
   
          <div className="chatbot-header">
            <div className="chatbot-headericon d-flex align-items-center flex-wrap">
              
              <h1 className="chatbot-header-text ms-0 text-wrap">Hospital ChatDB</h1>
            </div>
            <div className="chatbot-controls">
              <button onClick={openExitDialog} className="exit-button btn">
                <FontAwesomeIcon icon={faRotateRight} />
              </button>
              <button onClick={openLogoutDialog} className="logout-button btn">
                <FontAwesomeIcon icon={faRightFromBracket} />
              </button>
            </div>
          </div>
   
          {isChatVisible && (
            <div className="chat-window" ref={chatWindowRef} style={{ maxHeight: "80vh", overflowY: "auto" }}>
              
              {messages.length > 0 && (
                <div className="timestamp-header text-center">Today</div>
              )}
   
  {messages.map((msg, index) => (
    <div key={index} className={`message-wrapper ${msg.sender === "user" ? "user-message" : "bot-message"}`}>
   
     {msg.sender === "bot" && index < 2 && index === messages.length - 1 && (
                 <div className="chatbot-icon">
                  <FontAwesomeIcon icon={faUserNurse} />
                </div>  
              )}
   
              {msg.sender === 'bot' && index >= 1 && (
                <div className="chatbot-icon">
                  <FontAwesomeIcon icon={faUserNurse} />
                </div>
              )}
   
      <div className={`chat-bubble rounded-3`} style={{ backgroundColor: msg.sender === "user" ? '#43946d' : '#e5e5ea', color: msg.sender === "user" ? '#ffffff' : '#000000' }}>
        {msg.isTyping ? (
          <div className="typing-indicator d-flex">
            <span className="dot"></span>
            <span className="dot"></span>
            <span className="dot"></span>
          </div>
        ) : (
          msg.text.split('\n').map((line, i) => <p key={i} className="mb-0">{line}</p>)
        

        )}
      </div>
   
      {!msg.isTyping && (
        <div className={`timestamp-container ${msg.sender}-timestamp`}>
          {msg.timestamp}
        </div>
      )}
    </div>
  ))}
   
              {isExitDialogOpen && (
                
                <div className="exit-dialog">
                  <div className="dialog-content">
                    <div className="dialog-content-end">
                      <button onClick={endChat} className="btn">Restart Chat</button>
                    </div>
   
                    <div className="dialog-content-cancel">
                      <button onClick={closeExitDialog} className="btn btn-secondary">Cancel</button>
                    </div>
                  </div>
                </div>
                
              )}

              {isLogoutDialogOpen && (
                 <div className="overlay"> 
                <div className="exit-dialog">
                  <div className="dialog-content">
                    <div className="dialog-content-end">
                      <button onClick={onLogout} className="btn">Logout</button>
                    </div>
   
                    <div className="dialog-content-cancel">
                      <button onClick={closeLogoutDialog} className="btn btn-secondary">Cancel</button>
                    </div>
                  </div>
                </div>
                </div>
              )}
            </div>
          )}
   
  {showExampleQuestions && (
    <div className="message-wrapper example-questions d-flex flex-wrap justify-content-center gap-2">
      {exampleQuestions.map((question, index) => (
        <button
          key={index}
          className="btn example-question"
          onClick={() => handleExampleQuestionClick(question)}
          disabled={isStartNewChatDialogOpen}  
        >
          {question}
        </button>
      ))}
    </div>
  )}  
   
  <div className="input-area d-flex">
  <input
    id="us
    er-input"
    type="text"
    value={input}
    onChange={(e) => setInput(e.target.value)}
    onKeyPress={handleKeyPress}
    className="form-control"
    placeholder="Message..."
  />
    {input && (
     <button
     id="send-button"
     onClick={() => handleSendMessage()}
     className="btn"
     style={{
       pointerEvents: messages.some((msg) => msg.isTyping) ? 'none' : 'auto',
       opacity: messages.some((msg) => msg.isTyping) ? 1 : 1
     }}
  >
     <FontAwesomeIcon icon={faPaperPlane} />
  </button>
    )}
  </div>
    
        </div>

      </>
    );
  };
   
  export default Chatbot;
