using Microsoft.WindowsAzure.Storage.Table;

namespace SelfService.Server.Models
{
    public class HomePageEntity : TableEntity
    {
        public HomePageEntity()
        {
            this.PartitionKey = "homepage";
        }
        public string Message { get; set; }
    }
}