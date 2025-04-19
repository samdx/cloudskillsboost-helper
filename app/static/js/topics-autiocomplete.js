    // Autocomplete for topics
    document.addEventListener('DOMContentLoaded', function() {
        // Get the topics from the Flask template
        const topicsData = {{ topics | tojson }};

        // Transform the topicsData array to the desired format
        const formattedTopics = topicsData.map((topic, index) => ({
            id: index + 1,
            text: topic
        }));

        const elems = document.querySelectorAll('.autocomplete');
        const instances = M.Autocomplete.init(elems, {
            // specify options here
            minLength: 0, // shows instantly
            data: formattedTopics
        });
  });
