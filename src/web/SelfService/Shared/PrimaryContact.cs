using System.Collections.Generic;

namespace SelfService.Shared
{
    public class PrimaryContact
    {
        public string Primary { get; set; }
        public IEnumerable<User> Users { get; set; }
    }
}