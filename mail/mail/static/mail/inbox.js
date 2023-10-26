document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Event listeners for buttons
  document.querySelector('#compose-submit').addEventListener('click', send_email);
  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = ''; 

}

function load_mailbox(mailbox) {
  console.log('Enter load_mailbox function')
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none'
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Loading mails previews
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Print emails
    console.log(emails);
    // Load emails
    emails.forEach(load_mailbox_email)
});
  
}

function send_email() {
  console.log('Enter send_email function')
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: document.querySelector('#compose-recipients').value,
      subject: document.querySelector('#compose-subject').value,
      body: document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json())
  .then(result => {
    console.log(result)
    if (result.message == undefined){alert(result.error)};
    if (result.error == undefined){alert(result.message)};
  });
  load_mailbox('sent')
  location.reload()
}

function load_mailbox_email(contents) {
  console.log('Enter load_mailbox_email function')
  // Create new email preview in mailbox
  const email = document.createElement('div');
  email.className = 'email';
  email.id = contents.id;
  email.innerHTML = `${contents.subject}<br> ${contents.sender} at ${contents.timestamp}`;

  if (contents.read == true){
    email.style.backgroundColor = 'lightgrey'
  } else {
    email.style.backgroundColor = 'white'
  }
  
  email.addEventListener('click', function() {
    console.log(`CLICK on email with ID: ${email.id}`)
    fetch(`/emails/${email.id}`)
    .then(response => response.json())
    .then(email => {
      
      archiveButton = document.querySelector('#email-view-archive')
      replyButton = document.querySelector('#email-view-reply')

      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'none';
      document.querySelector('#email-view').style.display = 'block'
  
      document.querySelector('#email-view-sender').innerHTML = '<b>Sender: </b>' + email.sender
      document.querySelector('#email-view-recipients').innerHTML = '<b>Recipients: </b>' + email.recipients
      document.querySelector('#email-view-subject').innerHTML = '<b>Subject: </b>' + email.subject
      document.querySelector('#email-view-timestamp').innerHTML = '<b>Timestamp: </b>' + email.timestamp
      document.querySelector('#email-view-content').innerHTML = email.body
      
      replyButton.addEventListener('click', function() {
        console.log(`CLICK on REPLY button in email with ID: ${email.id}`)

        document.querySelector('#emails-view').style.display = 'none';
        document.querySelector('#compose-view').style.display = 'block';
        document.querySelector('#email-view').style.display = 'none'

        document.querySelector('#compose-recipients').value = email.sender;
        if (email.subject.slice(0, 3) === 'Re:') {
          document.querySelector('#compose-subject').value = `${email.subject}`;
        } else {
          document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
        }
        
        document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;

      })

      if (email.archived === true){
        archiveButton.innerHTML = 'Unarchive'
        archiveButton.addEventListener('click', () => archive_email(false, email.id))
      } else {
        archiveButton.innerHTML = 'Archive'
        archiveButton.addEventListener('click', () => archive_email(true, email.id))
      }
    });
    fetch(`/emails/${email.id}`, { method: 'PUT', body: JSON.stringify({ read: true }) })
  })
  // Add email preview to DOM
  document.querySelector('#emails-view').append(email);
  console.log(`APPEND email with ID: ${email.id} in #emails-view.`)
}

function archive_email(type, email_id){
  console.log(`CLICK on ARCHIVE/UNARCHIVE button in email with ID: ${email_id}`)
  fetch(`/emails/${email_id}`, { method: 'PUT', body: JSON.stringify({ archived: type }) })
  load_mailbox('inbox')
  location.reload()
}