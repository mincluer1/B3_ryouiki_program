// Authorization token that must have been created previously. See : https://developer.spotify.com/documentation/web-api/concepts/authorization
const token = 'BQA_Sn7HojNPmbdSqX_KuJA-SrGbeBvKg546CnjumjlQo7AmxzWIaaDbhEPo4qzxHvGrnb05zSasYGpbmredejaJgWgTU8eZHvWHhya1ZUyIyl79m3kwXixMjEsgZsLXXnfLWc7i-1ghz0C9oQrzyGg6dLdmmVpNPTiwqGGjGhVvwh7FJfcfRJMAvSV69mBPNAyww_iFSk4KsCs0OPwtZcm6_VqAdCFBDF9LxnnkaaNwmb7hZXb6WYQqYMHjArcXM6FYqpyZBAZ_AMxgG6iAcISwnwXeHIQ2ke7-VGQrAF_xfVCmCnFaFbfLRgnT';
async function fetchWebApi(endpoint, method, body) {
  const res = await fetch(`https://api.spotify.com/${endpoint}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
    method,
    body:JSON.stringify(body)
  });
  return await res.json();
}

async function getTopTracks(){
  // Endpoint reference : https://developer.spotify.com/documentation/web-api/reference/get-users-top-artists-and-tracks
  return (await fetchWebApi(
    'v1/me/top/tracks?time_range=long_term&limit=5', 'GET'
  )).items;
}

(async () => {
    const topTracks = await getTopTracks();
    console.log(
      topTracks?.map(
        ({ name, artists }) =>
          `${name} by ${artists.map(artist => artist.name).join(', ')}`
      )
    );
  })();
  