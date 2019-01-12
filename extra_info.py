"""Extra info"""
EXTRA = {
    '84': [
        {
            'title': 'Improved state restoring.',
            'content': "This comes with a downside: we will be unable to restore states the first time you start 0.84. This means that on upgrade to 0.84 any automation that doesn't have an initial_state defined will be disabled.",
            'more_info': None,
            'more_info_type': 'int' 
        }
    ],
    '85': [
        {
            'title': 'Changes in slugify.',
            'content': "Slugify changed, which impacts entity ID creation if the entities had names with characters that are not alphanumerical, these characters are now _ (underscore)",
            'more_info': '#19192',
            'more_info_type': 'int' 
        }
    ]
}
