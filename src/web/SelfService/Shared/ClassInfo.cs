using System;

namespace SelfService.Shared
{
    public class ClassInfo
    {
        public string Id { get; set; }
        public DateTime DateTime { get; set; }
        public string ClassName { get; set; }
        public string FriendlyDate
        {
            get
            {
                // this is currently issue in blazor web assembly
                // https://github.com/jsakamoto/Toolbelt.Blazor.TimeZoneKit/
                // which has been fixed in preview. But when consumed we had other issues
                // Need to consume as separate task.
                // var zone = TimeZoneInfo.FindSystemTimeZoneById("Pacific Standard Time");
                // var pst = TimeZoneInfo.ConvertTimeFromUtc(this.DateTime, zone);
                // return pst.ToString("MM-dd");

                // workaround for now
                return DateTime.ToString("MM-dd");
            }
        }
        public string FriendlyId { get => Id.Replace("-", ""); }
    }
}