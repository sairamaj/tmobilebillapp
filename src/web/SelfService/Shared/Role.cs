using System.Collections.Generic;

namespace SelfService.Shared
{
    public class Role
    {
        public string Name { get; set; }  
        public IEnumerable<string> Users {get; set;}
    }
}