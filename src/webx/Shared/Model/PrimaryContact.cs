using System.Collections.Generic;

namespace web.Shared.Model
{
    internal class PrimaryContact
    {
        public string Primary { get; set; }
        public IEnumerable<User> Users {get; set;}
    }
}