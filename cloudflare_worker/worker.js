addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const url = new URL(request.url)
  
  // Your Render app URL
  const flaskApiUrl = 'https://claims-management-final-1.onrender.com'

  // Extract claim_id from the URL path if available
  const claimId = url.pathname.split('/')[2]

  // Construct the API endpoint for the claim
  let apiUrl = `${flaskApiUrl}/claim`
  if (claimId) {
    apiUrl += `/${claimId}`
  }

  const options = {
    method: request.method,
    headers: request.headers,
    body: ['POST', 'PUT'].includes(request.method) ? await request.text() : null, // Only include body for POST/PUT
  }

  try {
    // Send request to Flask app
    const apiResponse = await fetch(apiUrl, options)
    
    // Return the response from Flask app to the client
    return new Response(await apiResponse.text(), {
      status: apiResponse.status,
      headers: apiResponse.headers,
    })
  } catch (error) {
    // Handle error if the Flask API fails to respond
    return new Response('Error fetching data from Flask API', { status: 500 })
  }
}
