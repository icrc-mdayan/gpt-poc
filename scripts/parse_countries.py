from bs4 import BeautifulSoup

# Sample HTML snippet provided by the user
html_snippet = '''<select data-drupal-selector="edit-country-id" id="edit-country-id" name="country_id" class="form-select select2-widget o-btn o-btn--ui select2-hidden-accessible" data-select2-config="{&quot;multiple&quot;:false,&quot;placeholder&quot;:&quot;Search for a country&quot;,&quot;allowClear&quot;:true,&quot;dir&quot;:&quot;ltr&quot;,&quot;language&quot;:&quot;en&quot;,&quot;tags&quot;:false,&quot;theme&quot;:&quot;healthdata&quot;,&quot;maximumSelectionLength&quot;:0,&quot;tokenSeparators&quot;:[],&quot;selectOnClose&quot;:false,&quot;width&quot;:&quot;100%&quot;,&quot;dropdownParent&quot;:&quot;#country-id-select2-element-wrapper&quot;}" aria-label="country selection" data-once="select2-init" data-select2-id="edit-country-id" tabindex="-1" aria-hidden="true"><option value="5381" data-select2-id="13">Afghanistan</option><option value="5325" data-select2-id="14">Albania</option><option value="5369" data-select2-id="15">Algeria</option><option value="5426" data-select2-id="16">American Samoa</option><option value="5287" data-select2-id="17">Andorra</option><option value="" selected="selected" data-select2-id="2"></option><option value="5405" data-select2-id="18">Angola</option><option value="5382" data-select2-id="19">Antigua and Barbuda</option><option value="5375" data-select2-id="20">Argentina</option><option value="5423" data-select2-id="21">Armenia</option><option value="5431" data-select2-id="22">Australia</option><option value="5466" data-select2-id="23">Austria</option><option value="5302" data-select2-id="24">Azerbaijan</option><option value="5411" data-select2-id="25">Bahrain</option><option value="5330" data-select2-id="26">Bangladesh</option><option value="5328" data-select2-id="27">Barbados</option><option value="5332" data-select2-id="28">Belarus</option><option value="5313" data-select2-id="29">Belgium</option><option value="5374" data-select2-id="30">Belize</option><option value="5409" data-select2-id="31">Benin</option><option value="5472" data-select2-id="32">Bermuda</option><option value="5412" data-select2-id="33">Bhutan</option><option value="5469" data-select2-id="34">Bolivia</option><option value="5339" data-select2-id="35">Bosnia and Herzegovina</option><option value="5345" data-select2-id="36">Botswana</option><option value="5479" data-select2-id="37">Brazil</option><option value="6552" data-select2-id="38">Brazil - Acre</option><option value="6553" data-select2-id="39">Brazil - Alagoas</option><option value="6554" data-select2-id="40">Brazil - Amapá</option><option value="6555" data-select2-id="41">Brazil - Amazonas</option><option value="6556" data-select2-id="42">Brazil - Bahia</option><option value="6557" data-select2-id="43">Brazil - Ceará</option><option value="6558" data-select2-id="44">Brazil - Distrito Federal</option><option value="6559" data-select2-id="45">Brazil - Espírito Santo</option><option value="6560" data-select2-id="46">Brazil - Goiás</option><option value="6561" data-select2-id="47">Brazil - Maranhão</option><option value="6562" data-select2-id="48">Brazil - Mato Grosso</option><option value="6563" data-select2-id="49">Brazil - Mato Grosso do Sul</option><option value="6564" data-select2-id="50">Brazil - Minas Gerais</option><option value="6565" data-select2-id="51">Brazil - Pará</option><option value="6566" data-select2-id="52">Brazil - Paraíba</option><option value="6567" data-select2-id="53">Brazil - Paraná</option><option value="6568" data-select2-id="54">Brazil - Pernambuco</option><option value="6569" data-select2-id="55">Brazil - Piaui</option><option value="6570" data-select2-id="56">Brazil - Rio de Janeiro</option><option value="6571" data-select2-id="57">Brazil - Rio Grande do Norte</option><option value="6572" data-select2-id="58">Brazil - Rio Grande do Sul</option><option value="6573" data-select2-id="59">Brazil - Rondônia</option><option value="6574" data-select2-id="60">Brazil - Roraima</option><option value="6575" data-select2-id="61">Brazil - Santa Catarina</option><option value="6576" data-select2-id="62">Brazil - São Paulo</option><option value="6577" data-select2-id="63">Brazil - Sergipe</option><option value="6578" data-select2-id="64">Brazil - Tocantins</option><option value="5312" data-select2-id="65">Brunei</option><option value="5360" data-select2-id="66">Bulgaria</option><option value="5346" data-select2-id="67">Burkina Faso</option><option value="5380" data-select2-id="68">Burundi</option><option value="5395" data-select2-id="69">Cambodia</option><option value="5297" data-select2-id="70">Cameroon</option><option value="5310" data-select2-id="71">Canada</option><option value="5435" data-select2-id="72">Cape Verde</option><option value="5347" data-select2-id="73">Central African Republic</option><option value="5338" data-select2-id="74">Chad</option><option value="5322" data-select2-id="75">Chile</option><option value="5317" data-select2-id="76">China</option><option value="5441" data-select2-id="77">Colombia</option><option value="5361" data-select2-id="78">Comoros</option><option value="5454" data-select2-id="79">Congo</option><option value="7701" data-select2-id="80">Cook Islands</option><option value="5386" data-select2-id="81">Costa Rica</option><option value="5384" data-select2-id="82">Cote d'Ivoire</option><option value="5470" data-select2-id="83">Croatia</option><option value="5400" data-select2-id="84">Cuba</option><option value="5420" data-select2-id="85">Cyprus</option><option value="5455" data-select2-id="86">Czech Republic</option><option value="5353" data-select2-id="87">Democratic Republic of the Congo</option><option value="5459" data-select2-id="88">Denmark</option><option value="5471" data-select2-id="89">Djibouti</option><option value="5410" data-select2-id="90">Dominica</option><option value="5326" data-select2-id="91">Dominican Republic</option><option value="5448" data-select2-id="92">Ecuador</option><option value="5461" data-select2-id="93">Egypt</option><option value="5365" data-select2-id="94">El Salvador</option><option value="5429" data-select2-id="95">Equatorial Guinea</option><option value="5311" data-select2-id="96">Eritrea</option><option value="5370" data-select2-id="97">Estonia</option><option value="5366" data-select2-id="98">Ethiopia</option><option value="9659" data-select2-id="99">Ethiopia - Addis Ababa</option><option value="9660" data-select2-id="100">Ethiopia - Afar</option><option value="9661" data-select2-id="101">Ethiopia - Amhara</option><option value="9662" data-select2-id="102">Ethiopia - Benishangul-Gumuz</option><option value="9663" data-select2-id="103">Ethiopia - Dire Dawa</option><option value="9664" data-select2-id="104">Ethiopia - Gambella</option><option value="9665" data-select2-id="105">Ethiopia - Harari</option><option value="9666" data-select2-id="106">Ethiopia - Oromia</option><option value="9667" data-select2-id="107">Ethiopia - Somali</option><option value="9668" data-select2-id="108">Ethiopia - Southern Nations, Nationalities, and Peoples</option><option value="9669" data-select2-id="109">Ethiopia - Tigray</option><option value="5385" data-select2-id="110">Federated States of Micronesia</option><option value="5453" data-select2-id="111">Fiji</option><option value="5464" data-select2-id="112">Finland</option><option value="5407" data-select2-id="113">France</option><option value="5465" data-select2-id="114">Gabon</option><option value="5457" data-select2-id="115">Georgia</option><option value="5286" data-select2-id="116">Germany</option><option value="5427" data-select2-id="117">Ghana</option><option value="5447" data-select2-id="118">Greece</option><option value="5373" data-select2-id="119">Greenland</option><option value="5354" data-select2-id="120">Grenada</option><option value="5467" data-select2-id="121">Guam</option><option value="5335" data-select2-id="122">Guatemala</option><option value="5440" data-select2-id="123">Guinea</option><option value="5351" data-select2-id="124">Guinea-Bissau</option><option value="5392" data-select2-id="125">Guyana</option><option value="5377" data-select2-id="126">Haiti</option><option value="5294" data-select2-id="127">Honduras</option><option value="5438" data-select2-id="128">Hungary</option><option value="5419" data-select2-id="129">Iceland</option><option value="5463" data-select2-id="130">India</option><option value="11462" data-select2-id="131">India - Andhra Pradesh</option><option value="11463" data-select2-id="132">India - Arunachal Pradesh</option><option value="11464" data-select2-id="133">India - Assam</option><option value="11465" data-select2-id="134">India - Bihar</option><option value="11466" data-select2-id="135">India - Chhattisgarh</option><option value="11467" data-select2-id="136">India - Delhi</option><option value="11468" data-select2-id="137">India - Goa</option><option value="11469" data-select2-id="138">India - Gujarat</option><option value="11470" data-select2-id="139">India - Haryana</option><option value="11471" data-select2-id="140">India - Himachal Pradesh</option><option value="11472" data-select2-id="141">India - Jammu &amp; Kashmir and Ladakh</option><option value="11473" data-select2-id="142">India - Jharkhand</option><option value="11474" data-select2-id="143">India - Karnataka</option><option value="11475" data-select2-id="144">India - Kerala</option><option value="11476" data-select2-id="145">India - Madhya Pradesh</option><option value="11477" data-select2-id="146">India - Maharashtra</option><option value="11478" data-select2-id="147">India - Manipur</option><option value="11479" data-select2-id="148">India - Meghalaya</option><option value="11480" data-select2-id="149">India - Mizoram</option><option value="11481" data-select2-id="150">India - Nagaland</option><option value="11482" data-select2-id="151">India - Odisha</option><option value="11483" data-select2-id="152">India - Other Union Territories</option><option value="11484" data-select2-id="153">India - Punjab</option><option value="11485" data-select2-id="154">India - Rajasthan</option><option value="11486" data-select2-id="155">India - Sikkim</option><option value="11487" data-select2-id="156">India - Tamil Nadu</option><option value="11488" data-select2-id="157">India - Telangana</option><option value="11489" data-select2-id="158">India - Tripura</option><option value="11490" data-select2-id="159">India - Uttar Pradesh</option><option value="11491" data-select2-id="160">India - Uttarakhand</option><option value="11492" data-select2-id="161">India - West Bengal</option><option value="5417" data-select2-id="162">Indonesia</option><option value="6698" data-select2-id="163">Indonesia - Aceh</option><option value="6699" data-select2-id="164">Indonesia - Bali</option><option value="6700" data-select2-id="165">Indonesia - Bangka-Belitung Islands</option><option value="6701" data-select2-id="166">Indonesia - Banten</option><option value="6702" data-select2-id="167">Indonesia - Bengkulu</option><option value="6707" data-select2-id="168">Indonesia - Central Java</option><option value="6711" data-select2-id="169">Indonesia - Central Kalimantan</option><option value="6725" data-select2-id="170">Indonesia - Central Sulawesi</option><option value="6708" data-select2-id="171">Indonesia - East Java</option><option value="6712" data-select2-id="172">Indonesia - East Kalimantan</option><option value="6719" data-select2-id="173">Indonesia - East Nusa Tenggara</option><option value="6703" data-select2-id="174">Indonesia - Gorontalo</option><option value="6704" data-select2-id="175">Indonesia - Jakarta</option><option value="6705" data-select2-id="176">Indonesia - Jambi</option><option value="6715" data-select2-id="177">Indonesia - Lampung</option><option value="6716" data-select2-id="178">Indonesia - Maluku</option><option value="6713" data-select2-id="179">Indonesia - North Kalimantan</option><option value="6717" data-select2-id="180">Indonesia - North Maluku</option><option value="6727" data-select2-id="181">Indonesia - North Sulawesi</option><option value="6730" data-select2-id="182">Indonesia - North Sumatra</option><option value="6720" data-select2-id="183">Indonesia - Papua</option><option value="6722" data-select2-id="184">Indonesia - Riau</option><option value="6714" data-select2-id="185">Indonesia - Riau Islands</option><option value="6710" data-select2-id="186">Indonesia - South Kalimantan</option><option value="6724" data-select2-id="187">Indonesia - South Sulawesi</option><option value="6729" data-select2-id="188">Indonesia - South Sumatra</option><option value="6726" data-select2-id="189">Indonesia - Southeast Sulawesi</option><option value="6706" data-select2-id="190">Indonesia - West Java</option><option value="6709" data-select2-id="191">Indonesia - West Kalimantan</option><option value="6718" data-select2-id="192">Indonesia - West Nusa Tenggara</option><option value="6721" data-select2-id="193">Indonesia - West Papua</option><option value="6723" data-select2-id="194">Indonesia - West Sulawesi</option><option value="6728" data-select2-id="195">Indonesia - West Sumatra</option><option value="6731" data-select2-id="196">Indonesia - Yogyakarta</option><option value="5449" data-select2-id="197">Iran</option><option value="9726" data-select2-id="198">Iran - Alborz</option><option value="9727" data-select2-id="199">Iran - Ardebil</option><option value="9728" data-select2-id="200">Iran - Bushehr</option><option value="9729" data-select2-id="201">Iran - Chahar Mahaal and Bakhtiari</option><option value="9730" data-select2-id="202">Iran - East Azarbayejan</option><option value="9731" data-select2-id="203">Iran - Fars</option><option value="9732" data-select2-id="204">Iran - Gilan</option><option value="9733" data-select2-id="205">Iran - Golestan</option><option value="9734" data-select2-id="206">Iran - Hamadan</option><option value="9735" data-select2-id="207">Iran - Hormozgan</option><option value="9736" data-select2-id="208">Iran - Ilam</option><option value="9737" data-select2-id="209">Iran - Isfahan</option><option value="9738" data-select2-id="210">Iran - Kerman</option><option value="9739" data-select2-id="211">Iran - Kermanshah</option><option value="9740" data-select2-id="212">Iran - Khorasan-e-Razavi</option><option value="9741" data-select2-id="213">Iran - Khuzestan</option><option value="9742" data-select2-id="214">Iran - Kohgiluyeh and Boyer-Ahmad</option><option value="9743" data-select2-id="215">Iran - Kurdistan</option><option value="9744" data-select2-id="216">Iran - Lorestan</option><option value="9745" data-select2-id="217">Iran - Markazi</option><option value="9746" data-select2-id="218">Iran - Mazandaran</option><option value="9747" data-select2-id="219">Iran - North Khorasan</option><option value="9748" data-select2-id="220">Iran - Qazvin</option><option value="9749" data-select2-id="221">Iran - Qom</option><option value="9750" data-select2-id="222">Iran - Semnan</option><option value="9751" data-select2-id="223">Iran - Sistan and Baluchistan</option><option value="9752" data-select2-id="224">Iran - South Khorasan</option><option value="9753" data-select2-id="225">Iran - Tehran</option><option value="9754" data-select2-id="226">Iran - West Azarbayejan</option><option value="9755" data-select2-id="227">Iran - Yazd</option><option value="9756" data-select2-id="228">Iran - Zanjan</option><option value="5301" data-select2-id="229">Iraq</option><option value="5288" data-select2-id="230">Ireland</option><option value="5304" data-select2-id="231">Israel</option><option value="5356" data-select2-id="232">Italy</option><option value="5421" data-select2-id="233">Jamaica</option><option value="5334" data-select2-id="234">Japan</option><option value="6019" data-select2-id="235">Japan - Aichi</option><option value="6020" data-select2-id="236">Japan - Akita</option><option value="6021" data-select2-id="237">Japan - Aomori</option><option value="6022" data-select2-id="238">Japan - Chiba</option><option value="6023" data-select2-id="239">Japan - Ehime</option><option value="6024" data-select2-id="240">Japan - Fukui</option><option value="6025" data-select2-id="241">Japan - Fukuoka</option><option value="6026" data-select2-id="242">Japan - Fukushima</option><option value="6027" data-select2-id="243">Japan - Gifu</option><option value="6028" data-select2-id="244">Japan - Gunma</option><option value="6029" data-select2-id="245">Japan - Hiroshima</option><option value="6030" data-select2-id="246">Japan - Hokkaidō</option><option value="6031" data-select2-id="247">Japan - Hyōgo</option><option value="6032" data-select2-id="248">Japan - Ibaraki</option><option value="6033" data-select2-id="249">Japan - Ishikawa</option><option value="6034" data-select2-id="250">Japan - Iwate</option><option value="6035" data-select2-id="251">Japan - Kagawa</option><option value="6036" data-select2-id="252">Japan - Kagoshima</option><option value="6037" data-select2-id="253">Japan - Kanagawa</option><option value="6038" data-select2-id="254">Japan - Kōchi</option><option value="6039" data-select2-id="255">Japan - Kumamoto</option><option value="6040" data-select2-id="256">Japan - Kyōto</option><option value="6041" data-select2-id="257">Japan - Mie</option><option value="6042" data-select2-id="258">Japan - Miyagi</option><option value="6043" data-select2-id="259">Japan - Miyazaki</option><option value="6044" data-select2-id="260">Japan - Nagano</option><option value="6045" data-select2-id="261">Japan - Nagasaki</option><option value="6046" data-select2-id="262">Japan - Nara</option><option value="6047" data-select2-id="263">Japan - Niigata</option><option value="6048" data-select2-id="264">Japan - Ôita</option><option value="6049" data-select2-id="265">Japan - Okayama</option><option value="6050" data-select2-id="266">Japan - Okinawa</option><option value="6051" data-select2-id="267">Japan - Ōsaka</option><option value="6052" data-select2-id="268">Japan - Saga</option><option value="6053" data-select2-id="269">Japan - Saitama</option><option value="6054" data-select2-id="270">Japan - Shiga</option><option value="6055" data-select2-id="271">Japan - Shimane</option><option value="6056" data-select2-id="272">Japan - Shizuoka</option><option value="6057" data-select2-id="273">Japan - Tochigi</option><option value="6058" data-select2-id="274">Japan - Tokushima</option><option value="6059" data-select2-id="275">Japan - Tōkyō</option><option value="6060" data-select2-id="276">Japan - Tottori</option><option value="6061" data-select2-id="277">Japan - Toyama</option><option value="6062" data-select2-id="278">Japan - Wakayama</option><option value="6063" data-select2-id="279">Japan - Yamagata</option><option value="6064" data-select2-id="280">Japan - Yamaguchi</option><option value="6065" data-select2-id="281">Japan - Yamanashi</option><option value="5383" data-select2-id="282">Jordan</option><option value="5319" data-select2-id="283">Kazakhstan</option><option value="5352" data-select2-id="284">Kenya</option><option value="8405" data-select2-id="285">Kenya - Baringo</option><option value="8407" data-select2-id="286">Kenya - Bomet</option><option value="8408" data-select2-id="287">Kenya - Bungoma</option><option value="8409" data-select2-id="288">Kenya - Busia</option><option value="8410" data-select2-id="289">Kenya - Elgeyo-Marakwet</option><option value="8411" data-select2-id="290">Kenya - Embu</option><option value="8412" data-select2-id="291">Kenya - Garissa</option><option value="8413" data-select2-id="292">Kenya - HomaBay</option><option value="8414" data-select2-id="293">Kenya - Isiolo</option><option value="8415" data-select2-id="294">Kenya - Kajiado</option><option value="8416" data-select2-id="295">Kenya - Kakamega</option><option value="8417" data-select2-id="296">Kenya - Kericho</option><option value="8418" data-select2-id="297">Kenya - Kiambu</option><option value="8419" data-select2-id="298">Kenya - Kilifi</option><option value="8421" data-select2-id="299">Kenya - Kirinyaga</option><option value="8423" data-select2-id="300">Kenya - Kisii</option><option value="8425" data-select2-id="301">Kenya - Kisumu</option><option value="8427" data-select2-id="302">Kenya - Kitui</option><option value="8429" data-select2-id="303">Kenya - Kwale</option><option value="8431" data-select2-id="304">Kenya - Laikipia</option><option value="8433" data-select2-id="305">Kenya - Lamu</option><option value="8435" data-select2-id="306">Kenya - Machakos</option><option value="8437" data-select2-id="307">Kenya - Makueni</option><option value="8439" data-select2-id="308">Kenya - Mandera</option><option value="8406" data-select2-id="309">Kenya - Marsabit</option><option value="8420" data-select2-id="310">Kenya - Meru</option><option value="8422" data-select2-id="311">Kenya - Migori</option><option value="8424" data-select2-id="312">Kenya - Mombasa</option><option value="8426" data-select2-id="313">Kenya - Murang'a</option><option value="8428" data-select2-id="314">Kenya - Nairobi</option><option value="8430" data-select2-id="315">Kenya - Nakuru</option><option value="8432" data-select2-id="316">Kenya - Nandi</option><option value="8434" data-select2-id="317">Kenya - Narok</option><option value="8436" data-select2-id="318">Kenya - Nyamira</option><option value="8438" data-select2-id="319">Kenya - Nyandarua</option><option value="8440" data-select2-id="320">Kenya - Nyeri</option><option value="8441" data-select2-id="321">Kenya - Samburu</option><option value="8442" data-select2-id="322">Kenya - Siaya</option><option value="8443" data-select2-id="323">Kenya - Taita-Taveta</option><option value="8444" data-select2-id="324">Kenya - Tana River</option><option value="8445" data-select2-id="325">Kenya - Tharaka-Nithi</option><option value="8446" data-select2-id="326">Kenya - Trans-Nzoia</option><option value="8447" data-select2-id="327">Kenya - Turkana</option><option value="8448" data-select2-id="328">Kenya - Uasin Gishu</option><option value="8449" data-select2-id="329">Kenya - Vihiga</option><option value="8450" data-select2-id="330">Kenya - Wajir</option><option value="8451" data-select2-id="331">Kenya - West Pokot</option><option value="5444" data-select2-id="332">Kiribati</option><option value="5344" data-select2-id="333">Kuwait</option><option value="5303" data-select2-id="334">Kyrgyzstan</option><option value="5358" data-select2-id="335">Laos</option><option value="5439" data-select2-id="336">Latvia</option><option value="5474" data-select2-id="337">Lebanon</option><option value="5481" data-select2-id="338">Lesotho</option><option value="5415" data-select2-id="339">Liberia</option><option value="5290" data-select2-id="340">Libya</option><option value="5443" data-select2-id="341">Lithuania</option><option value="5396" data-select2-id="342">Luxembourg</option><option value="5399" data-select2-id="343">Macedonia</option><option value="5320" data-select2-id="344">Madagascar</option><option value="5484" data-select2-id="345">Malawi</option><option value="5343" data-select2-id="346">Malaysia</option><option value="5318" data-select2-id="347">Maldives</option><option value="5475" data-select2-id="348">Mali</option><option value="5477" data-select2-id="349">Malta</option><option value="5389" data-select2-id="350">Marshall Islands</option><option value="5437" data-select2-id="351">Mauritania</option><option value="5480" data-select2-id="352">Mauritius</option><option value="5413" data-select2-id="353">Mexico</option><option value="6066" data-select2-id="354">Mexico - Aguascalientes</option><option value="6067" data-select2-id="355">Mexico - Baja California</option><option value="6068" data-select2-id="356">Mexico - Baja California Sur</option><option value="6069" data-select2-id="357">Mexico - Campeche</option><option value="6070" data-select2-id="358">Mexico - Chiapas</option><option value="6071" data-select2-id="359">Mexico - Chihuahua</option><option value="6072" data-select2-id="360">Mexico - Coahuila</option><option value="6073" data-select2-id="361">Mexico - Colima</option><option value="6074" data-select2-id="362">Mexico - Distrito Federal</option><option value="6075" data-select2-id="363">Mexico - Durango</option><option value="6076" data-select2-id="364">Mexico - Guanajuato</option><option value="6077" data-select2-id="365">Mexico - Guerrero</option><option value="6078" data-select2-id="366">Mexico - Hidalgo</option><option value="6079" data-select2-id="367">Mexico - Jalisco</option><option value="6080" data-select2-id="368">Mexico - México</option><option value="6081" data-select2-id="369">Mexico - Michoacán de Ocampo</option><option value="6082" data-select2-id="370">Mexico - Morelos</option><option value="6083" data-select2-id="371">Mexico - Nayarit</option><option value="6084" data-select2-id="372">Mexico - Nuevo León</option><option value="6085" data-select2-id="373">Mexico - Oaxaca</option><option value="6086" data-select2-id="374">Mexico - Puebla</option><option value="6087" data-select2-id="375">Mexico - Querétaro</option><option value="6088" data-select2-id="376">Mexico - Quintana Roo</option><option value="6089" data-select2-id="377">Mexico - San Luis Potosí</option><option value="6090" data-select2-id="378">Mexico - Sinaloa</option><option value="6091" data-select2-id="379">Mexico - Sonora</option><option value="6092" data-select2-id="380">Mexico - Tabasco</option><option value="6093" data-select2-id="381">Mexico - Tamaulipas</option><option value="6094" data-select2-id="382">Mexico - Tlaxcala</option><option value="6095" data-select2-id="383">Mexico - Veracruz de Ignacio de la Llave</option><option value="6096" data-select2-id="384">Mexico - Yucatán</option><option value="6097" data-select2-id="385">Mexico - Zacatecas</option><option value="5367" data-select2-id="386">Moldova</option><option value="5422" data-select2-id="387">Mongolia</option><option value="5340" data-select2-id="388">Montenegro</option><option value="5414" data-select2-id="389">Morocco</option><option value="5305" data-select2-id="390">Mozambique</option><option value="5368" data-select2-id="391">Myanmar</option><option value="5314" data-select2-id="392">Namibia</option><option value="5293" data-select2-id="393">Nepal</option><option value="5350" data-select2-id="394">Netherlands</option><option value="5289" data-select2-id="395">New Zealand</option><option value="5306" data-select2-id="396">Nicaragua</option><option value="5402" data-select2-id="397">Niger</option><option value="5376" data-select2-id="398">Nigeria</option><option value="5388" data-select2-id="399">North Korea</option><option value="5387" data-select2-id="400">Northern Mariana Islands</option><option value="5355" data-select2-id="401">Norway</option><option value="9950" data-select2-id="402">Norway - Agder</option><option value="9951" data-select2-id="403">Norway - Innlandet</option><option value="9952" data-select2-id="404">Norway - Møre og Romsdal</option><option value="9953" data-select2-id="405">Norway - Nordland</option><option value="9954" data-select2-id="406">Norway - Oslo</option><option value="9955" data-select2-id="407">Norway - Rogaland</option><option value="9956" data-select2-id="408">Norway - Troms og Finnmark</option><option value="9957" data-select2-id="409">Norway - Trøndelag</option><option value="9958" data-select2-id="410">Norway - Vestfold og Telemark</option><option value="9959" data-select2-id="411">Norway - Vestland</option><option value="9960" data-select2-id="412">Norway - Viken</option><option value="5446" data-select2-id="413">Oman</option><option value="5434" data-select2-id="414">Pakistan</option><option value="9797" data-select2-id="415">Pakistan - Azad Jammu &amp; Kashmir</option><option value="9798" data-select2-id="416">Pakistan - Balochistan</option><option value="9799" data-select2-id="417">Pakistan - Gilgit-Baltistan</option><option value="9800" data-select2-id="418">Pakistan - Islamabad Capital Territory</option><option value="9801" data-select2-id="419">Pakistan - Khyber Pakhtunkhwa</option><option value="9802" data-select2-id="420">Pakistan - Punjab</option><option value="9803" data-select2-id="421">Pakistan - Sindh</option><option value="5296" data-select2-id="422">Palestine</option><option value="5456" data-select2-id="423">Panama</option><option value="5291" data-select2-id="424">Papua New Guinea</option><option value="5348" data-select2-id="425">Paraguay</option><option value="5442" data-select2-id="426">Peru</option><option value="5309" data-select2-id="427">Philippines</option><option value="5473" data-select2-id="428">Poland</option><option value="5315" data-select2-id="429">Portugal</option><option value="7702" data-select2-id="430">Principality of Monaco</option><option value="5393" data-select2-id="431">Puerto Rico</option><option value="5451" data-select2-id="432">Qatar</option><option value="7704" data-select2-id="433">Republic of Nauru</option><option value="7705" data-select2-id="434">Republic of Niue</option><option value="7706" data-select2-id="435">Republic of Palau</option><option value="7703" data-select2-id="436">Republic of San Marino</option><option value="5482" data-select2-id="437">Romania</option><option value="5329" data-select2-id="438">Russia</option><option value="5298" data-select2-id="439">Rwanda</option><option value="7707" data-select2-id="440">Saint Kitts and Nevis</option><option value="5460" data-select2-id="441">Saint Lucia</option><option value="5445" data-select2-id="442">Saint Vincent and the Grenadines</option><option value="5316" data-select2-id="443">Samoa</option><option value="5476" data-select2-id="444">Sao Tome and Principe</option><option value="5406" data-select2-id="445">Saudi Arabia</option><option value="5308" data-select2-id="446">Senegal</option><option value="5430" data-select2-id="447">Serbia</option><option value="5371" data-select2-id="448">Seychelles</option><option value="5336" data-select2-id="449">Sierra Leone</option><option value="5363" data-select2-id="450">Singapore</option><option value="5292" data-select2-id="451">Slovakia</option><option value="5450" data-select2-id="452">Slovenia</option><option value="5391" data-select2-id="453">Solomon Islands</option><option value="5342" data-select2-id="454">Somalia</option><option value="5331" data-select2-id="455">South Africa</option><option value="9476" data-select2-id="456">South Africa - Eastern Cape</option><option value="9477" data-select2-id="457">South Africa - Free State</option><option value="9478" data-select2-id="458">South Africa - Gauteng</option><option value="9479" data-select2-id="459">South Africa - KwaZulu-Natal</option><option value="9480" data-select2-id="460">South Africa - Limpopo</option><option value="9481" data-select2-id="461">South Africa - Mpumalanga</option><option value="9482" data-select2-id="462">South Africa - North-West</option><option value="9483" data-select2-id="463">South Africa - Northern Cape</option><option value="9484" data-select2-id="464">South Africa - Western Cape</option><option value="5364" data-select2-id="465">South Korea</option><option value="5321" data-select2-id="466">South Sudan</option><option value="5416" data-select2-id="467">Spain</option><option value="5337" data-select2-id="468">Sri Lanka</option><option value="5357" data-select2-id="469">Sudan</option><option value="5462" data-select2-id="470">Suriname</option><option value="5418" data-select2-id="471">Swaziland</option><option value="5299" data-select2-id="472">Sweden</option><option value="5625" data-select2-id="473">Sweden - Stockholm</option><option value="5626" data-select2-id="474">Sweden - Sweden except Stockholm</option><option value="5424" data-select2-id="475">Switzerland</option><option value="5394" data-select2-id="476">Syria</option><option value="5362" data-select2-id="477">Taiwan (Province of China)</option><option value="5403" data-select2-id="478">Tajikistan</option><option value="5379" data-select2-id="479">Tanzania</option><option value="5327" data-select2-id="480">Thailand</option><option value="5372" data-select2-id="481">The Bahamas</option><option value="5324" data-select2-id="482">The Gambia</option><option value="5452" data-select2-id="483">Timor-Leste</option><option value="5333" data-select2-id="484">Togo</option><option value="7708" data-select2-id="485">Tokelau</option><option value="5359" data-select2-id="486">Tonga</option><option value="5401" data-select2-id="487">Trinidad and Tobago</option><option value="5295" data-select2-id="488">Tunisia</option><option value="5458" data-select2-id="489">Turkey</option><option value="5408" data-select2-id="490">Turkmenistan</option><option value="7709" data-select2-id="491">Tuvalu</option><option value="5433" data-select2-id="492">Uganda</option><option value="5436" data-select2-id="493">Ukraine</option><option value="5468" data-select2-id="494">United Arab Emirates</option><option value="5378" data-select2-id="495">United Kingdom</option><option value="5323" data-select2-id="496">United Kingdom - England</option><option value="6010" data-select2-id="497">United Kingdom - England - East Midlands</option><option value="6011" data-select2-id="498">United Kingdom - England - East of England</option><option value="6012" data-select2-id="499">United Kingdom - England - Greater London</option><option value="6013" data-select2-id="500">United Kingdom - England - North East England</option><option value="6014" data-select2-id="501">United Kingdom - England - North West England</option><option value="6015" data-select2-id="502">United Kingdom - England - South East England</option><option value="6016" data-select2-id="503">United Kingdom - England - South West England</option><option value="6017" data-select2-id="504">United Kingdom - England - West Midlands</option><option value="6018" data-select2-id="505">United Kingdom - England - Yorkshire and the Humber</option><option value="5341" data-select2-id="506">United Kingdom - Northern Ireland</option><option value="5483" data-select2-id="507">United Kingdom - Scotland</option><option value="5404" data-select2-id="508">United Kingdom - Wales</option><option value="5390" data-select2-id="509">United States</option><option value="6349" data-select2-id="510">United States - Alabama</option><option value="6350" data-select2-id="511">United States - Alaska</option><option value="6351" data-select2-id="512">United States - Arizona</option><option value="6352" data-select2-id="513">United States - Arkansas</option><option value="6353" data-select2-id="514">United States - California</option><option value="6354" data-select2-id="515">United States - Colorado</option><option value="6355" data-select2-id="516">United States - Connecticut</option><option value="6356" data-select2-id="517">United States - Delaware</option><option value="6357" data-select2-id="518">United States - District of Columbia</option><option value="6358" data-select2-id="519">United States - Florida</option><option value="6359" data-select2-id="520">United States - Georgia</option><option value="6360" data-select2-id="521">United States - Hawaii</option><option value="6361" data-select2-id="522">United States - Idaho</option><option value="6362" data-select2-id="523">United States - Illinois</option><option value="6363" data-select2-id="524">United States - Indiana</option><option value="6364" data-select2-id="525">United States - Iowa</option><option value="6365" data-select2-id="526">United States - Kansas</option><option value="6366" data-select2-id="527">United States - Kentucky</option><option value="6367" data-select2-id="528">United States - Louisiana</option><option value="6368" data-select2-id="529">United States - Maine</option><option value="6369" data-select2-id="530">United States - Maryland</option><option value="6370" data-select2-id="531">United States - Massachusetts</option><option value="6371" data-select2-id="532">United States - Michigan</option><option value="6372" data-select2-id="533">United States - Minnesota</option><option value="6373" data-select2-id="534">United States - Mississippi</option><option value="6374" data-select2-id="535">United States - Missouri</option><option value="6375" data-select2-id="536">United States - Montana</option><option value="6376" data-select2-id="537">United States - Nebraska</option><option value="6377" data-select2-id="538">United States - Nevada</option><option value="6378" data-select2-id="539">United States - New Hampshire</option><option value="6379" data-select2-id="540">United States - New Jersey</option><option value="6380" data-select2-id="541">United States - New Mexico</option><option value="6381" data-select2-id="542">United States - New York</option><option value="6382" data-select2-id="543">United States - North Carolina</option><option value="6383" data-select2-id="544">United States - North Dakota</option><option value="6384" data-select2-id="545">United States - Ohio</option><option value="6385" data-select2-id="546">United States - Oklahoma</option><option value="6386" data-select2-id="547">United States - Oregon</option><option value="6387" data-select2-id="548">United States - Pennsylvania</option><option value="6388" data-select2-id="549">United States - Rhode Island</option><option value="6389" data-select2-id="550">United States - South Carolina</option><option value="6390" data-select2-id="551">United States - South Dakota</option><option value="6391" data-select2-id="552">United States - Tennessee</option><option value="6392" data-select2-id="553">United States - Texas</option><option value="6393" data-select2-id="554">United States - Utah</option><option value="6394" data-select2-id="555">United States - Vermont</option><option value="6395" data-select2-id="556">United States - Virginia</option><option value="6396" data-select2-id="557">United States - Washington</option><option value="6397" data-select2-id="558">United States - West Virginia</option><option value="6398" data-select2-id="559">United States - Wisconsin</option><option value="6399" data-select2-id="560">United States - Wyoming</option><option value="5307" data-select2-id="561">Uruguay</option><option value="5485" data-select2-id="562">Uzbekistan</option><option value="5397" data-select2-id="563">Vanuatu</option><option value="5398" data-select2-id="564">Venezuela</option><option value="5428" data-select2-id="565">Vietnam</option><option value="5349" data-select2-id="566">Virgin Islands, U.S.</option><option value="5478" data-select2-id="567">Yemen</option><option value="5425" data-select2-id="568">Zambia</option><option value="5432" data-select2-id="569">Zimbabwe</option></select>'''

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(html_snippet, 'html.parser')

# Find all <option> tags
options = soup.find_all('option')

# Extract the text (country names) and store them in a list, excluding any empty values
countries = [option.text for option in options if option.text.strip()]

# Output the list of countries
print(countries)
print(len(countries))