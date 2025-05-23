# Handling Graduation

When students graduate need to make sure they get the alumni role and remove the student role.
The bot handles this by watching for emoji reactions on a particular message. The emoji used for this is 🥳.


Example Message
```
@Students
Graduating seniors - 
Congrats on graduating 🎉 ! It is time to say good bye to your Student role and continue the celebration with your Alumni Role

To do so please react 🥳 to this message

(Please don't react to this message if you haven't graduated as it removes your student role)
```

### Process

1. Send the message, or a different one, above to the students channel
2. Get the message ID of the message sent. You will need developers mode enabled to do this. To enable developer mode:
   - Go to your profile in the bottom left > Edit Profile > Advanced > Developer Mode
   - Right click on the message and select "Copy ID"
3. Use `/set-graduation` with the message ID to set the message the bot will watch for reactions on