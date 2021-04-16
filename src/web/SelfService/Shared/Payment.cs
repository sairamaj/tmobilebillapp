using System;
using System.Linq;

namespace SelfService.Shared
{
    public class Payment
    {
        public string Name { get; set; }
        public string Type { get; set; }
        public double Amount { get; set; }
        public DateTime Date { get; set; }
        public string DateString => Date.ToString("MM/dd/yyyy");
        public string Method { get; set; }
        public string Comment { get; set; }
        public string User {
            get{
                var parts = this.Type.Split('_');
                if( parts.Length > 2){
                    return parts[1];
                }
                return "NA";
            }
        }
    }
}
