var mongoose     = require('mongoose');
var Schema       = mongoose.Schema;

var FeedSchema   = new Schema({
    message: String,
    authorID: String
});

module.exports = mongoose.model('Feed', FeedSchema);
